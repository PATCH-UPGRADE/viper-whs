// RFB shim because the way novnc is packaged their typing doesn't get picked up automatically
declare module '@novnc/novnc/core/rfb.js' {
    export default class RFB {
        constructor(
            target: HTMLElement,
            url: string,
            options?: {
                credentials?: { password?: string };
                wsProtocols?: string[];
                shared?: boolean;
            }
        )

        disconnect(): void;
        sendCredentials(creds: { password: string }): void;
        addEventListener(type: string, listener: EventListenerOrEventListenerObject): void;
        removeEventListener(type: string, listener: EventListenerOrEventListenerObject): void;
        scaleViewport: boolean;
        resizeSession: boolean;
        viewOnly: boolean;
        qualityLevel: number;
        compressionLevel: number;
    }
}
