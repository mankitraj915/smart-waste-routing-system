import React from 'react';
import { Play, Loader2, CheckCircle2 } from 'lucide-react';

function ControlPanel({ processState, onTrigger }) {
    const loading = ['INGESTING', 'PREDICTING', 'OPTIMIZING'].includes(processState);

    return (
        <div className="flex flex-col gap-4">
            <div>
                <h2 className="text-xs font-bold tracking-[0.1em] text-zinc-900 uppercase">Routing Engine</h2>
                <div className="mt-3 p-6 bg-white rounded-2xl border border-zinc-200/60 shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)] transition-shadow hover:shadow-md duration-500">
                    <p className="text-sm text-zinc-500 mb-6 leading-relaxed">
                        Dispatch the asynchronous swarm logic to generate the most efficient execution paths.
                    </p>
                    
                    <button 
                        onClick={onTrigger} 
                        disabled={loading}
                        className={`
                            relative overflow-hidden flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-medium w-full transition-all duration-300
                            ${loading 
                                ? 'bg-zinc-100 text-zinc-400 cursor-not-allowed' 
                                : 'bg-primary text-white hover:bg-primary-hover shadow-md shadow-primary/20 hover:-translate-y-0.5 active:translate-y-0'}
                        `}
                    >
                        {loading ? (
                            <>
                                <Loader2 className="animate-spin text-primary" size={18} />
                                <span className="text-zinc-700">
                                    {processState === 'INGESTING' ? 'Ingesting...' : processState === 'PREDICTING' ? 'Predicting...' : 'Optimizing...'}
                                </span>
                            </>
                        ) : (
                            <>
                                <Play size={18} className="fill-current" />
                                Initiate Dispatch
                            </>
                        )}
                    </button>

                    {processState === 'COMPLETED' && (
                        <div className="mt-4 flex items-center justify-center gap-2 text-sm font-medium text-emerald-600 bg-emerald-50 py-2.5 rounded-xl border border-emerald-100/50 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <CheckCircle2 size={16} />
                            Routes Synchronized
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ControlPanel;
