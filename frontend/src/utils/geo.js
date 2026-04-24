export const isSamePoint = (a, b) => {
    if (!a || !b) return false;
    
    // Support array [lat, lng] or object {coords: [lat, lng]} or {lat, lng}
    const latA = Array.isArray(a) ? a[0] : (a.coords ? a.coords[0] : a.lat);
    const lngA = Array.isArray(a) ? a[1] : (a.coords ? a.coords[1] : a.lng);
    
    const latB = Array.isArray(b) ? b[0] : (b.coords ? b.coords[0] : b.lat);
    const lngB = Array.isArray(b) ? b[1] : (b.coords ? b.coords[1] : b.lng);

    if (latA == null || lngA == null || latB == null || lngB == null) return false;

    return Math.abs(latA - latB) < 1e-5 && Math.abs(lngA - lngB) < 1e-5;
};

export const isNodeInRoute = (node, activeRoute) => {
    if (!node || !Array.isArray(activeRoute)) return false;
    return activeRoute.some(p => isSamePoint(p, node));
};
