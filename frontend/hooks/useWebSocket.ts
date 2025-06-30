import { useEffect, useRef, useState, useCallback } from 'react'

interface UseWebSocketOptions {
  url: string
  onOpen?: () => void
  onClose?: () => void
  onMessage?: (data: any) => void
  onError?: (error: Event) => void
}

export function useWebSocket({
  url,
  onOpen,
  onClose,
  onMessage,
  onError,
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return

    const ws = new WebSocket(url)
    
    ws.onopen = () => {
      setIsConnected(true)
      onOpen?.()
    }
    
    ws.onclose = () => {
      setIsConnected(false)
      onClose?.()
    }
    
    ws.onmessage = (event) => {
      const data = event.data instanceof Blob 
        ? event.data 
        : JSON.parse(event.data)
      onMessage?.(data)
    }
    
    ws.onerror = (error) => {
      onError?.(error)
    }
    
    wsRef.current = ws
  }, [url, onOpen, onClose, onMessage, onError])

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [])

  const send = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        typeof data === 'string' ? data : JSON.stringify(data)
      )
    }
  }, [])

  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [disconnect])

  return {
    isConnected,
    connect,
    disconnect,
    send,
  }
}