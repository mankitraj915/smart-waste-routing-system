import React from 'react';
import { 
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    BarChart, Bar, Cell, AreaChart, Area
} from 'recharts';
import { convergenceData, distanceComparison, predictionAccuracy, nodePruning } from '../../data/researchData';

function ResearchPanel() {
    return (
        <div className="h-full w-full bg-white rounded-[2rem] border border-blue-200/60 shadow-[0_4px_20px_-4px_rgba(37,99,235,0.05)] overflow-hidden relative fade-in p-8 flex flex-col gap-6 overflow-y-auto">
            <div className="flex flex-col gap-2 pb-2 border-b border-zinc-100">
                <div className="flex items-center gap-3">
                    <span className="bg-blue-100 text-blue-700 text-xs font-bold px-2 py-1 rounded-md uppercase tracking-widest">Research Validation Mode</span>
                </div>
                <h2 className="text-2xl font-bold text-zinc-900 tracking-tight">Experimentally Validated Results</h2>
                <p className="text-sm text-zinc-500 font-medium">Historical metrics extracted directly from the system's foundational research phase. Not live data.</p>
            </div>

            {/* TOP: Dominant Convergence Chart */}
            <div className="flex flex-col gap-4 border border-zinc-200/60 bg-zinc-50/30 p-6 rounded-2xl">
                <h3 className="text-sm font-bold text-zinc-800 uppercase tracking-wider">Algorithmic Convergence Efficiency</h3>
                <div className="h-[250px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={convergenceData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e4e4e7" />
                            <XAxis dataKey="iteration" tick={{fontSize: 12, fill: '#71717a'}} axisLine={false} tickLine={false} />
                            <YAxis domain={['auto', 'auto']} tick={{fontSize: 12, fill: '#71717a'}} axisLine={false} tickLine={false} />
                            <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                            <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                            <Line type="monotone" dataKey="ga" name="GA" stroke="#ef4444" strokeWidth={2} dot={false} />
                            <Line type="monotone" dataKey="aco" name="ACO" stroke="#eab308" strokeWidth={2} dot={false} />
                            <Line type="monotone" dataKey="hybrid" name="Hybrid GA-ACO" stroke="#2563eb" strokeWidth={3} dot={false} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
                <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 mt-2">
                    <p className="text-sm text-blue-900/80 leading-relaxed">
                        <strong className="text-blue-700">Explanation:</strong> This chart plots optimization iterations against total path cost. 
                        Pure GA suffers from slow convergence, and pure ACO has a delayed start due to pheromone buildup. 
                        The <strong>Hybrid GA-ACO</strong> model inherently mitigates both flaws, securing the global minimum significantly faster.
                    </p>
                </div>
            </div>

            {/* MIDDLE: Distance Comparison and Prediction Accuracy */}
            <div className="grid grid-cols-2 gap-6">
                
                {/* Distance Chart */}
                <div className="flex flex-col gap-4 border border-zinc-200/60 bg-zinc-50/30 p-6 rounded-2xl">
                    <h3 className="text-sm font-bold text-zinc-800 uppercase tracking-wider">Distance Reduction (~38%)</h3>
                    <div className="h-[200px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={distanceComparison} layout="vertical" margin={{ top: 0, right: 30, left: 10, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e4e4e7" />
                                <XAxis type="number" tick={{fontSize: 12, fill: '#71717a'}} axisLine={false} tickLine={false} />
                                <YAxis dataKey="name" type="category" tick={{fontSize: 12, fill: '#71717a', fontWeight: 'bold'}} axisLine={false} tickLine={false} />
                                <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                                <Bar dataKey="distance" radius={[0, 4, 4, 0]} barSize={24}>
                                    {distanceComparison.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.name === 'Predictive' ? '#2563eb' : '#94a3b8'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 mt-2 h-full">
                        <p className="text-sm text-blue-900/80 leading-relaxed">
                            <strong className="text-blue-700">Explanation:</strong> 
                            Applying the predictive pruning layer to the routing algorithm yields a <strong>~38% reduction</strong> in driving distance compared to static schedules, vastly decreasing fuel consumption.
                        </p>
                    </div>
                </div>

                {/* Prediction Chart */}
                <div className="flex flex-col gap-4 border border-zinc-200/60 bg-zinc-50/30 p-6 rounded-2xl">
                    <h3 className="text-sm font-bold text-zinc-800 uppercase tracking-wider">RMSE Accuracy Gain</h3>
                    <div className="h-[200px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={predictionAccuracy} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e4e4e7" />
                                <XAxis dataKey="model" tick={{fontSize: 12, fill: '#71717a', fontWeight: 'bold'}} axisLine={false} tickLine={false} />
                                <YAxis tick={{fontSize: 12, fill: '#71717a'}} axisLine={false} tickLine={false} />
                                <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                                <Bar dataKey="rmse" radius={[4, 4, 0, 0]} barSize={40}>
                                    {predictionAccuracy.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.model.includes('XGBoost') ? '#10b981' : '#f87171'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 mt-2 h-full">
                        <p className="text-sm text-blue-900/80 leading-relaxed">
                            <strong className="text-blue-700">Explanation:</strong> 
                            A pure LSTM struggles with nonlinear anomalies. Ensembling it with XGBoost cuts the Root Mean Square Error (RMSE) in half, ensuring fewer overflowing bins are missed.
                        </p>
                    </div>
                </div>

            </div>

            {/* BOTTOM: Node Pruning */}
            <div className="flex flex-col border border-emerald-200/60 bg-emerald-50/30 p-6 rounded-2xl">
                <h3 className="text-sm font-bold text-emerald-900 uppercase tracking-wider mb-6">Computational Search Space Reduction</h3>
                <div className="flex items-center justify-between gap-8">
                    <div className="flex flex-1 items-center justify-center gap-6">
                        <div className="flex flex-col items-center">
                            <span className="text-5xl font-bold text-zinc-800">{nodePruning.total}</span>
                            <span className="text-xs font-bold text-zinc-500 uppercase tracking-widest mt-2">Total Monitored Nodes</span>
                        </div>
                        <div className="text-zinc-300 font-light text-4xl">➜</div>
                        <div className="flex flex-col items-center">
                            <span className="text-5xl font-bold text-emerald-600">{nodePruning.active}</span>
                            <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest mt-2">Priority Dispatched</span>
                        </div>
                    </div>
                    <div className="flex-1 bg-white border border-emerald-100 rounded-xl p-5 shadow-sm">
                        <p className="text-sm text-emerald-900/80 leading-relaxed">
                            <strong className="text-emerald-700">Explanation:</strong> 
                            By filtering out nodes with ample remaining capacity via ML prediction, the system mathematically pruned 
                            the geographic search space by <strong>{((nodePruning.total - nodePruning.active) / nodePruning.total * 100).toFixed(1)}%</strong>. 
                            This exponentially accelerates Swarm optimization compute times on the backend.
                        </p>
                    </div>
                </div>
            </div>

        </div>
    );
}

export default ResearchPanel;
