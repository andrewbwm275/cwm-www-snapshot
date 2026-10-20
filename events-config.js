// Public, non-secret config for first-party conversion events. OFF by default.
// IT: set enabled:true once POST /api/event exists. Payload: {"type":"tel_click|sms_click|form_submit","page":"/path/"}
window.__CWM_EVENTS__ = { enabled: false, endpoint: "/api/event" };
