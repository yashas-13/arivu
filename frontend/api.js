(function(){
    const API_BASE = '';
    function getAuthHeaders() {
        const token = localStorage.getItem('token');
        return token ? { 'Authorization': 'Bearer ' + token } : {};
    }
    window.apiFetch = async function(url, options = {}) {
        options.headers = { ...(options.headers || {}), ...getAuthHeaders() };
        const resp = await fetch(API_BASE + url, options);
        if (!resp.ok && (resp.status === 401 || resp.status === 403)) {
            localStorage.removeItem('token');
            window.location.href = '/index.html';
        }
        return resp;
    };
})();
