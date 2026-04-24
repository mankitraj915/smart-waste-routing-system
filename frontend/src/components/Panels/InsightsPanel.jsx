import React, { useMemo } from 'react';
import { Package, Route, Zap, Activity, Target } from 'lucide-react';
import ProcessTimeline from './ProcessTimeline';
import { isNodeInRoute } from '../../utils/geo';

function InsightCard({ title, value, icon: Icon, delay }) {
    return (
        <div 
            className="group flex flex-col p-5 bg-white rounded-2xl border border-zinc-200/60 shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)] hover:shadow-lg hover:border-primary/20 transition-all duration-500 animate-in fade-in slide-in-from-bottom-4" 
            style={{ animationDelay: `${delay}ms`, animationFillMode: 'both' }}
        >
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2.5 bg-blue-50 text-primary rounded-xl group-hover:scale-110 transition-transform duration-300 shrink-0">
                    <Icon size={18} />
                </div>
                <p className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest">{title}</p>
            </div>
            <p className="text-3xl font-bold text-zinc-900 tracking-tight ml-1">{value}</p>
        </div>
    );
}

function InsightsPanel({ processState, nodes, metrics, activeRoute }) {
    const hasData = processState !== 'IDLE';
    const isComplete = processState === 'COMPLETED';
    
    const activeNodes = useMemo(() => {
        if (!hasData || !nodes) return 0;
        return nodes.filter(n => isNodeInRoute(n, activeRoute)).length;
    }, [hasData, nodes, activeRoute]);
    
    let improvement = "0%";
    let distReduction = "0";
    if (isComplete && metrics.initialDist && metrics.finalDist) {
        const imp = ((metrics.initialDist - metrics.finalDist) / metrics.initialDist) * 100;
        improvement = `${Math.max(0, imp).toFixed(1)}%`;
        distReduction = Math.max(0, metrics.initialDist - metrics.finalDist).toFixed(1);
    }

    return (
        <div className="flex flex-col gap-6">
            <div>
                <h2 className="text-xs font-bold tracking-[0.1em] text-zinc-900 uppercase">Execution Status</h2>
                <div className="mt-3 p-5 bg-white rounded-2xl border border-zinc-200/60 shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)]">
                    <ProcessTimeline currentState={processState} />
                </div>
            </div>

            <div className="flex flex-col gap-4">
                <h2 className="text-xs font-bold tracking-[0.1em] text-zinc-900 uppercase">Route Intelligence</h2>
                
                <div className="grid grid-cols-2 gap-4">
                    <InsightCard title="Total Nodes" value={hasData && nodes ? nodes.length : 0} icon={Package} delay={100} />
                    <InsightCard title="Selected Nodes" value={hasData ? activeNodes : 0} icon={Target} delay={150} />
                </div>
                
                <div className="flex flex-col gap-4">
                    <InsightCard 
                        title="Estimated Distance" 
                        value={isComplete ? `${metrics.finalDist}km` : (hasData && metrics.initialDist ? `~${metrics.initialDist}km` : '0km')} 
                        icon={Route} 
                        delay={200} 
                    />
                    <InsightCard 
                        title="Efficiency Gain" 
                        value={isComplete ? improvement : '0%'} 
                        icon={Zap} 
                        delay={300} 
                    />
                </div>
                <div className="flex flex-col gap-1 mt-1 text-xs text-gray-500 font-medium">
                    <p>• Optimized using Hybrid GA-ACO combining exploration and refinement.</p>
                    <p>• Low-priority nodes removed via predictive filtering.</p>
                </div>
            </div>

            {isComplete && (
                <div className="mt-2 p-5 bg-blue-50/60 rounded-2xl border border-blue-100/50 animate-in fade-in slide-in-from-bottom-2">
                    <h3 className="text-[11px] font-bold text-blue-900/70 uppercase tracking-widest mb-3">Optimization Summary</h3>
                    <ul className="text-[13px] text-blue-900/80 space-y-3 font-medium">
                        <li className="flex gap-2.5 items-start">
                            <span className="text-blue-500 mt-0.5">•</span> 
                            <span>Travel distance reduced by <strong className="text-blue-600">{distReduction}km</strong> compared to baseline approach.</span>
                        </li>
                        <li className="flex gap-2.5 items-start">
                            <span className="text-blue-500 mt-0.5">•</span> 
                            <span>Algorithm isolated <strong className="text-blue-600">{nodes.length - activeNodes} low-priority</strong> nodes to conserve fuel and time.</span>
                        </li>
                    </ul>
                </div>
            )}
        </div>
    );
}

export default InsightsPanel;
