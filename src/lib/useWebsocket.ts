import { useCallback, useEffect, useRef, useState } from "react";

export enum ReadyState {
  CONNECTING = 0,
  OPEN = 1,
  CLOSING = 2,
  CLOSED = 3,
}

export interface UseWebSocketOptions {
  onOpen?: (event: Event) => void;
  onMessage?: (event: MessageEvent) => void;
  onClose?: (event: CloseEvent) => void;
  onError?: (event: Event) => void;
  reconnect?: boolean;
  reconnectDelayMs?: number;
  maxRetries?: number;
}

export interface UseWebSocketReturn {
  readyState: ReadyState;
  lastMessage: MessageEvent | null;
  sendMessage: (data: string) => void;
  disconnect: () => void;
  connect: () => void;
}

function useWebSocket(
  url: string | null,
  opts: UseWebSocketOptions = {},
): UseWebSocketReturn {
  const {
    onOpen,
    onMessage,
    onClose,
    onError,
    reconnect = true,
    reconnectDelayMs = 3000,
    maxRetries = 5,
  } = opts;

  const [readyState, setReadyState] = useState<ReadyState>(ReadyState.CLOSED);
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const retryCountRef = useRef<number>(0);
  const retryTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const manualCloseRef = useRef<boolean>(false);

  // Keep the latest callbacks in refs so WebSocket handlers are never stale
  // without triggering unnecessary reconnects via the dependency array.
  const onOpenRef = useRef<UseWebSocketOptions["onOpen"]>(onOpen);
  const onMessageRef = useRef<UseWebSocketOptions["onMessage"]>(onMessage);
  const onCloseRef = useRef<UseWebSocketOptions["onClose"]>(onClose);
  const onErrorRef = useRef<UseWebSocketOptions["onError"]>(onError);

  useEffect(() => {
    onOpenRef.current = onOpen;
  }, [onOpen]);
  useEffect(() => {
    onMessageRef.current = onMessage;
  }, [onMessage]);
  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);
  useEffect(() => {
    onErrorRef.current = onError;
  }, [onError]);

  const clearRetryTimer = useCallback((): void => {
    if (retryTimerRef.current !== null) {
      clearTimeout(retryTimerRef.current);
      retryTimerRef.current = null;
    }
  }, []);

  const connectWs = useCallback((): void => {
    if (!url) return;

    if (wsRef.current) {
      wsRef.current.onopen = null;
      wsRef.current.onmessage = null;
      wsRef.current.onclose = null;
      wsRef.current.onerror = null;
      wsRef.current.close();
    }

    const ws = new WebSocket(url);
    wsRef.current = ws;
    setReadyState(ReadyState.CONNECTING);

    ws.onopen = (event: Event): void => {
      retryCountRef.current = 0;
      setReadyState(ReadyState.OPEN);
      onOpenRef.current?.(event);
    };

    ws.onmessage = (event: MessageEvent): void => {
      setLastMessage(event);
      onMessageRef.current?.(event);
    };

    ws.onclose = (event: CloseEvent): void => {
      setReadyState(ReadyState.CLOSED);
      onCloseRef.current?.(event);

      const shouldRetry =
        !manualCloseRef.current &&
        reconnect &&
        (maxRetries === -1 || retryCountRef.current < maxRetries);

      if (shouldRetry) {
        retryCountRef.current += 1;
        retryTimerRef.current = setTimeout(() => {
          connectWs();
        }, reconnectDelayMs);
      }
    };

    ws.onerror = (event: Event): void => {
      onErrorRef.current?.(event);
    };
  }, [url, reconnect, reconnectDelayMs, maxRetries]);

  useEffect(() => {
    if (!url) return;

    manualCloseRef.current = false;
    retryCountRef.current = 0;
    connectWs();

    return (): void => {
      clearRetryTimer();
      manualCloseRef.current = true;
      if (wsRef.current) {
        wsRef.current.onopen = null;
        wsRef.current.onmessage = null;
        wsRef.current.onclose = null;
        wsRef.current.onerror = null;
        wsRef.current.close();
      }
    };
  }, [url, connectWs, clearRetryTimer]);

  const sendMessage = useCallback((data: string): void => {
    if (wsRef.current?.readyState === ReadyState.OPEN) {
      wsRef.current.send(data);
    } else {
      console.warn("[useWebSocket] Cannot send: socket is not open.");
    }
  }, []);

  const disconnect = useCallback((): void => {
    clearRetryTimer();
    manualCloseRef.current = true;
    if (wsRef.current) {
      setReadyState(ReadyState.CLOSING);
      wsRef.current.close();
    }
  }, [clearRetryTimer]);

  const connect = useCallback((): void => {
    manualCloseRef.current = false;
    retryCountRef.current = 0;
    connectWs();
  }, [connectWs]);

  return { readyState, lastMessage, sendMessage, disconnect, connect };
}

export default useWebSocket;
