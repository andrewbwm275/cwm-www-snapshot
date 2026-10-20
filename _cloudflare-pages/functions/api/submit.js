// Pages Function: same-origin /api/submit handled by the shared site-forms handler (lib/site-forms.js).
import handler from "../../lib/site-forms.js";
export const onRequest = ({ request, env }) => handler.fetch(request, env);
