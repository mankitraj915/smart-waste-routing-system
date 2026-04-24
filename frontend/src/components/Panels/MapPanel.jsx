import React, { useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Polyline, Popup, Marker, Tooltip } from 'react-leaflet';
import { Map as MapIcon } from 'lucide-react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { isSamePoint } from '../../utils/geo';

function MapPanel({ route, baselineRoute, nodes, baseLat, baseLng, isProcessing, isComplete, selectedNode, setSelectedNode }) {
    if (!nodes || nodes.length === 0) {
        return (
            <div className="h-full w-full bg-white rounded-[2rem] border border-zinc-200/60 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] flex flex-col items-center justify-center text-zinc-400 gap-5 transition-all duration-500">
                <div className="p-8 bg-zinc-50 rounded-full">
                    <MapIcon size={48} className="opacity-40" />
                </div>
                <p className="font-semibold tracking-wide text-zinc-400 uppercase text-sm">Map Interface Offline</p>
            </div>
        );
    }

    const getColor = (fill) => {
        if (fill >= 80) return "#ef4444"; // red
        if (fill >= 50) return "#eab308"; // yellow
        return "#22c55e"; // green
    };

    const createNumberedIcon = (num) => L.divIcon({
        className: 'custom-number-icon',
        html: `<div style="background-color: #2563EB; color: white; border-radius: 50%; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; border: 2px solid white; transform: translate(-9px, -9px); box-shadow: 0 2px 4px rgba(0,0,0,0.2);">${num}</div>`,
        iconSize: [0, 0],
        iconAnchor: [0, 0]
    });

    const renderedNodes = useMemo(() => {
        return nodes.map((node, idx) => {
            const isSelected = selectedNode?.id === node.id;
            return (
                <CircleMarker 
                    key={`node-${node.id}`}
                    center={node.coords} 
                    radius={isSelected ? 10 : 6}
                    eventHandlers={{ click: () => setSelectedNode(node) }}
                    pathOptions={{ 
                        color: isSelected ? "#3b82f6" : getColor(node.fill), 
                        fillColor: getColor(node.fill), 
                        fillOpacity: isSelected ? 1 : 0.8,
                        weight: isSelected ? 4 : 2
                    }}
                >
                    <Tooltip className="rounded-md font-bold shadow-sm" direction="top" offset={[0, -10]}>
                        Node {node.id}
                    </Tooltip>
                </CircleMarker>
            );
        });
    }, [nodes, selectedNode, setSelectedNode]);

    return (
        <div className="h-full w-full bg-white rounded-[2rem] border border-zinc-200/60 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] overflow-hidden relative fade-in">
            <MapContainer center={[baseLat, baseLng]} zoom={13} style={{ height: '100%', width: '100%', zIndex: 10 }}>
                <TileLayer
                    url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
                />
                
                {!isProcessing && baselineRoute && baselineRoute.length > 0 && (
                    <Polyline 
                        positions={baselineRoute} 
                        color="#a1a1aa" 
                        dashArray="4, 8"
                        weight={2} 
                        opacity={0.5} 
                        lineCap="round" 
                        lineJoin="round" 
                        interactive={false}
                    />
                )}

                {route && route.length > 0 && (
                    <Polyline 
                        positions={route} 
                        color={isProcessing ? "#94a3b8" : "#2563EB"} 
                        dashArray={isProcessing ? "10, 10" : null}
                        weight={isProcessing ? 3 : 5} 
                        opacity={isProcessing ? 0.6 : 0.85} 
                        lineCap="round" 
                        lineJoin="round" 
                        className={isProcessing ? "animate-pulse" : "transition-all duration-1000"}
                        interactive={false}
                    />
                )}

                {isComplete && route && route.map((pos, idx) => {
                    const matchedNode = nodes.find(n => isSamePoint(n, pos));
                    return (
                        <Marker 
                            key={`route-badge-${idx}`}
                            position={pos}
                            icon={createNumberedIcon(idx + 1)}
                            zIndexOffset={1000}
                            eventHandlers={matchedNode ? { click: () => setSelectedNode(matchedNode) } : {}}
                        />
                    );
                })}
                
                {renderedNodes}
            </MapContainer>
        </div>
    );
}

export default MapPanel;
