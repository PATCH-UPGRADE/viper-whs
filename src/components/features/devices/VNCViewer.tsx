import RFB from "@novnc/novnc/core/rfb.js";

export default class VncConnection {
  rfb: RFB;
  desktopName: string;

  statusElement: any;
  rfbElement: any;

  constructor() {
    this.desktopName = "";
    
    this.statusElement = document.getElementById('vncStatus');
    // const desktopNameElement = document.getElementById('vncScreen');
    this.rfbElement = document.getElementById('vncScreen');

    const host = this.readQueryVariable('host', window.location.hostname);
    const port = this.readQueryVariable('port', window.location.port);
    const password = this.readQueryVariable('password', "");
    const path = this.readQueryVariable('path', 'vnc_websocket');

    this.setStatus("Connecting...");

    const protocol = window.location.protocol === "https:" ? 'wss' : 'ws';
    const url = `${protocol}://${host}:${port}/${path}`;

    this.rfb = new RFB(this.rfbElement, url, {
        credentials: { password },
    });

    this.rfb.addEventListener("connect", (e: unknown) => this.onConnect(e));
    this.rfb.addEventListener("disconnect", (e: unknown) => this.onDisconnect(e));
    // this.rfb.addEventListener("credentialsrequired", (e: unknown) => this.onCredentialsRequired(e));
    this.rfb.addEventListener("desktopname", (e: unknown) => this.onDesktopName(e));

    // this.rfb.viewOnly = this.readQueryVariable("view_only", "false");
    // this.rfb.scaleViewport = this.readQueryVariable("scale", "false");

    document.getElementById("sendCtrlAltDel")?.addEventListener("click", (e: unknown) => {
        this.sendCtrlAltDel();
    })
  }

  setStatus(newStatus: string) {
      this.statusElement.textContent = newStatus;
  }

  onConnect(e: unknown) {
      this.setStatus(`Connected to ${this.desktopName}`);
  }

  onDisconnect(e: unknown) {
    if (e.detail.clean) {
      this.setStatus("Disconnected");
    } else {
      this.setStatus("Something went wrong - Connection closed!");
    }
  }

  onCredentialsRequired(e: unknown) {
    const password = prompt("Password required:");
    this.rfb.sendCredentials({ password });
  }

  onDesktopName(e: unknown) {
      this.desktopName = e.detail.name;
  }

  sendCtrlAltDel() {
      this.rfb.sendCtrlAltDel();
  }

  readQueryVariable(name: string, defaultValue: string) {
    const re = new RegExp('.*[?&]' + name + '=([^&#]*)');
    const match = document.location.href.match(re);

    if (match) {
      return decodeURIComponent(match[1]);
    }

    return defaultValue;
  }
};
