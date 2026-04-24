import React, { useMemo } from 'react';
import { Info, Target, Trash2, X } from 'lucide-react';
import { isNodeInRoute } from '../../utils/geo';

function NodeDetailsPanel({ selectedNode, activeRoute, setSelectedNode }) {
    const isSelected = useMemo(() => {
        return isNodeInRoute(selectedNode, activeRoute);
    }, [selectedNode, activeRoute]);

    const isOpen = !!selectedNode;
    const fillLevel = selectedNode?.fill ?? 'N/A';
    
    let priority = 'LOW';
    let priorityColor = 'text-zinc-600 bg-zinc-100';
    if (fillLevel !== 'N/A') {
        if (fillLevel >= 80) {
            priority = 'HIGH';
            priorityColor = 'text-rose-700 bg-rose-100';
        } else if (fillLevel >= 50) {
            priority = 'MEDIUM';
            priorityColor = 'text-amber-700 bg-amber-100';
        }
    }

    return (
        <div 
            className={`fixed right-0 top-0 z-50 w-[320px] h-full bg-white border-l border-zinc-200 shadow-2xl flex flex-col p-6 gap-6 overflow-y-auto transition-transform duration-500 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}
        >
            <button 
                onClick={() => setSelectedNode(null)} 
                className="absolute top-4 right-4 p-2 text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 rounded-full transition-colors"
            >
                <X size={20} />
            </button>
            
            {selectedNode ? (
                <>
                    <div className="flex flex-col gap-1 border-b border-zinc-100 pb-4 mt-8">
                        <h2 className="text-lg font-bold text-zinc-900 tracking-tight">Node #{selectedNode.id}</h2>
                        <p className="text-xs text-zinc-500 font-mono">
                            {selectedNode.coords?.[0]?.toFixed(4) ?? '0.0000'}, {selectedNode.coords?.[1]?.toFixed(4) ?? '0.0000'}
                        </p>
                    </div>

                    <div className="flex flex-col gap-4">
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-zinc-600">Fill Level</span>
                            <span className="text-sm font-bold text-zinc-900">{fillLevel}%</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-zinc-600">Priority</span>
                            <span className={`text-xs font-bold px-2 py-1 rounded-md tracking-wider ${priorityColor}`}>
                                {priority}
                            </span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-zinc-600">Status</span>
                            {isSelected ? (
                                <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-md tracking-wider border border-emerald-100">
                                    <Target size={12} /> SELECTED
                                </span>
                            ) : (
                                <span className="flex items-center gap-1.5 text-xs font-bold text-zinc-600 bg-zinc-100 px-2 py-1 rounded-md tracking-wider border border-zinc-200">
                                    <Trash2 size={12} /> SKIPPED
                                </span>
                            )}
                        </div>
                    </div>

                    <div className={`p-4 rounded-xl border mt-auto ${isSelected ? 'bg-blue-50 border-blue-100' : 'bg-zinc-50 border-zinc-200'}`}>
                        <h3 className={`text-xs font-bold uppercase tracking-wider mb-2 flex items-center gap-2 ${isSelected ? 'text-blue-800' : 'text-zinc-600'}`}>
                            <span className={`w-1.5 h-1.5 rounded-full ${isSelected ? 'bg-blue-500' : 'bg-zinc-400'}`}></span>
                            AI Decision Logic
                        </h3>
                        <p className={`text-sm leading-relaxed ${isSelected ? 'text-blue-900/80' : 'text-zinc-600'}`}>
                            {isSelected 
                                ? "Selected by the routing algorithm and included in the optimal path." 
                                : "Skipped by the algorithm to minimize unnecessary distance or due to low fill level."
                            }
                        </p>
                    </div>
                </>
            ) : (
                <div className="flex flex-col items-center justify-center h-full gap-4 text-zinc-400">
                    <Info size={32} className="opacity-50" />
                    <p className="text-sm font-medium">Select a node</p>
                </div>
            )}
        </div>
    );
}

export default NodeDetailsPanel;
