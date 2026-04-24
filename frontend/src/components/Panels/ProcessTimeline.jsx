import React from 'react';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

const steps = [
    { id: 'INGESTING', label: 'Ingesting Nodes' },
    { id: 'PREDICTING', label: 'Predictive Pruning' },
    { id: 'OPTIMIZING', label: 'Hybrid GA-ACO Optimization' },
    { id: 'COMPLETED', label: 'Route Synchronized' }
];

function ProcessTimeline({ currentState }) {
    const getStatus = (stepId) => {
        if (currentState === 'IDLE') return 'waiting';
        if (currentState === 'COMPLETED') return 'completed';
        
        const stateOrder = ['IDLE', 'INGESTING', 'PREDICTING', 'OPTIMIZING', 'COMPLETED'];
        const currentIndex = stateOrder.indexOf(currentState);
        const stepIndex = stateOrder.indexOf(stepId);
        
        if (currentIndex > stepIndex) return 'completed';
        if (currentIndex === stepIndex) return 'active';
        return 'waiting';
    };

    return (
        <div className="flex flex-col gap-4 mt-2">
            {steps.map((step, idx) => {
                const status = getStatus(step.id);
                return (
                    <div key={step.id} className="flex items-center gap-3">
                        <div className="flex flex-col items-center">
                            {status === 'completed' ? (
                                <CheckCircle2 size={18} className="text-emerald-500" />
                            ) : status === 'active' ? (
                                <Loader2 size={18} className="text-primary animate-spin" />
                            ) : (
                                <Circle size={18} className="text-zinc-300" />
                            )}
                            {idx !== steps.length - 1 && (
                                <div className={`w-0.5 h-6 my-1 rounded-full ${status === 'completed' ? 'bg-emerald-500' : 'bg-zinc-200'}`} />
                            )}
                        </div>
                        <span className={`text-sm font-medium ${status === 'active' ? 'text-zinc-900' : status === 'completed' ? 'text-zinc-700' : 'text-zinc-400'}`}>
                            {step.label}
                        </span>
                    </div>
                );
            })}
        </div>
    );
}

export default ProcessTimeline;
