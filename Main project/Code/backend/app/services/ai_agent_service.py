import logging
import os
import re
import concurrent.futures
from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

try:
    # Official SDK (preferred). Package: google-genai
    from google import genai  # type: ignore
except Exception:
    genai = None

try:
    # Unofficial fallback (often flaky, but keep as last resort)
    from g4f.client import Client  # type: ignore
except Exception:
    Client = None

logger = logging.getLogger(__name__)

class AIAgentService:
    """
    ASL concept extraction + robust mapping to available signs.

    Goal: for ANY input text, output a list of signs that actually exist
    in `available_signs`, by combining:
    - LLM keyword extraction (Gemini if configured; else g4f; else local)
    - Semantic mapping (sentence-transformers) from extracted keywords -> available signs
    """
    
    def __init__(self):
        self._embedder = None
        self._available_cache_key = None
        self._sign_embeddings = None
        self._sign_list = None

    def _get_embedder(self) -> SentenceTransformer:
        if self._embedder is None:
            model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            self._embedder = SentenceTransformer(model_name)
        return self._embedder

    def extract_asl_concepts(self, text: str, available_signs: Optional[List[str]] = None) -> List[str]:
        """
        Extract concepts from text and map to the closest available ASL signs.

        Returns only items that exist in `available_signs`.
        """
        if not text or not text.strip():
            return []

        available_signs = [s.strip().lower() for s in (available_signs or []) if s and s.strip()]
        if not available_signs:
            return self._local_keywords(text)[:10]

        prompt = self._build_keyword_prompt(text)

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._run_llm, prompt)
                keywords = future.result(timeout=30) or []
            
            logger.info(f"AI extracted concepts: {keywords}")
            mapped = self._map_keywords_to_available_signs(keywords, available_signs)
            return mapped
            
        except Exception as e:
            logger.error(f"Error calling AI agent: {str(e)}")
            local = self._local_keywords(text)
            return self._map_keywords_to_available_signs(local, available_signs)
            
    def _build_keyword_prompt(self, text: str) -> str:
        return f"""
You are an American Sign Language (ASL) keyword extraction agent.

Task:
- From the input text, output 5-12 SHORT keywords that capture the meaning.
- Prefer base forms (e.g., "teach" not "teaching").
- Remove filler words.
- Output ONLY a comma-separated list. No other text.

Text: "{text}"
Keywords:
""".strip()

    def _run_llm(self, prompt: str) -> List[str]:
        # 1) Prefer official Gemini if configured
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        if api_key and genai is not None:
            client = genai.Client(api_key=api_key)
            resp = client.models.generate_content(
                model=gemini_model,
                contents=prompt,
            )
            content = (getattr(resp, "text", "") or "").strip()
            return self._parse_keywords(content)

        # 2) Fallback to g4f (unofficial)
        if os.getenv("ENABLE_G4F", "").strip() in {"1", "true", "TRUE", "yes", "YES"} and Client is not None:
            client = Client()
            response = client.chat.completions.create(
                model=os.getenv("G4F_MODEL", "gemini-2.0-flash"),
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content.strip()
            return self._parse_keywords(content)

        # 3) Last resort: local keywording
        return self._local_keywords(prompt)

    def _parse_keywords(self, content: str) -> List[str]:
        # Keep it robust against "1) foo" / newlines / extra punctuation
        content = content.replace("\n", ",")
        parts = [p.strip().lower() for p in content.split(",")]
        cleaned = []
        for p in parts:
            p = re.sub(r"^[\s\d\-\)\.]+", "", p).strip()
            p = re.sub(r"[^a-z0-9\s]", "", p).strip()
            if p:
                cleaned.append(p)
        # Deduplicate while preserving order
        seen = set()
        out = []
        for k in cleaned:
            if k not in seen:
                seen.add(k)
                out.append(k)
        return out

    def _local_keywords(self, text: str) -> List[str]:
        # Lightweight fallback: tokenize + drop stopwords
        words = re.findall(r"\b[\w']+\b", text.lower())
        stop = {
            "a","an","the","is","am","are","was","were","to","in","on","at","of","for","with","and","or","but",
            "i","you","he","she","it","we","they","me","my","your","our","their","this","that","these","those",
            "from","by","as","be","been","being","do","does","did","doing","have","has","had","having",
            "can","could","will","would","should","may","might","must",
        }
        keep = [w for w in words if w not in stop and len(w) > 1]
        # Deduplicate preserving order
        seen = set()
        out = []
        for w in keep:
            if w not in seen:
                seen.add(w)
                out.append(w)
        return out

    def _ensure_sign_embeddings(self, available_signs: List[str]) -> None:
        cache_key = "|".join(sorted(available_signs))
        if self._available_cache_key == cache_key and self._sign_embeddings is not None:
            return
        embedder = self._get_embedder()
        self._sign_list = available_signs
        self._sign_embeddings = embedder.encode(available_signs, convert_to_numpy=True, normalize_embeddings=True)
        self._available_cache_key = cache_key

    def _map_keywords_to_available_signs(self, keywords: List[str], available_signs: List[str]) -> List[str]:
        # Direct exact matches first
        available_set = set(available_signs)
        exact = [k for k in keywords if k in available_set]

        # Semantic map remaining keywords -> closest sign
        remaining = [k for k in keywords if k not in available_set]
        mapped = list(exact)

        if remaining:
            self._ensure_sign_embeddings(available_signs)
            embedder = self._get_embedder()
            kw_emb = embedder.encode(remaining, convert_to_numpy=True, normalize_embeddings=True)
            # cosine similarity since vectors are normalized
            sims = np.matmul(kw_emb, self._sign_embeddings.T)
            min_sim = float(os.getenv("ASL_SIGN_MIN_SIM", "0.35"))
            candidates = []
            for i, kw in enumerate(remaining):
                best_j = int(np.argmax(sims[i]))
                best_sim = float(sims[i][best_j])
                if best_sim >= min_sim:
                    candidates.append((best_sim, kw, self._sign_list[best_j]))

            # Prefer the strongest matches first
            candidates.sort(key=lambda t: t[0], reverse=True)
            for _sim, _kw, best_sign in candidates:
                if best_sign not in mapped:
                    mapped.append(best_sign)

        # If still empty, pick a safe small default from existing signs
        if not mapped:
            for fallback in ("hello", "learn", "together", "school", "teacher", "student"):
                if fallback in available_set:
                    mapped.append(fallback)
                    if len(mapped) >= 3:
                        break
            if not mapped:
                mapped = available_signs[:3]

        max_signs = int(os.getenv("ASL_MAX_SIGNS", "8"))
        return mapped[:max_signs]

    # Backwards-compatible alias (some older code may call this)
    def _fallback_extraction(self, text: str, available_signs: Optional[List[str]] = None) -> List[str]:
        local = self._local_keywords(text)
        if available_signs:
            return self._map_keywords_to_available_signs(local, [s.lower() for s in available_signs])
        return local

