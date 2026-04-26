import React from 'react'

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('[ErrorBoundary] Uncaught error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-8">
          <div className="text-5xl">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-800">Something went wrong</h1>
          <p className="text-gray-600 text-center max-w-md">
            {this.state.error?.message || 'An unexpected error occurred.'}
          </p>
          <button
            onClick={() => { this.setState({ hasError: false, error: null }); window.history.back() }}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Go Back
          </button>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
          >
            Reload Page
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
