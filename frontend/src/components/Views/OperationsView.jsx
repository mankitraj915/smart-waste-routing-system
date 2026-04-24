import React from 'react';
import MapPanel from '../Panels/MapPanel';
import ControlPanel from '../Panels/ControlPanel';
import InsightsPanel from '../Panels/InsightsPanel';
import NodeDetailsPanel from '../Panels/NodeDetailsPanel';

function OperationsView({ processState, nodes, activeRoute, baselineRoute, metrics, onTrigger, baseLat, baseLng, selectedNode, setSelectedNode }) {
  return (
      <div className="max-w-[1600px] mx-auto h-full flex flex-col gap-6 fade-in">
          <div className="flex flex-col gap-1 border-b border-zinc-200/60 pb-4">
            <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">Operations</h1>
            <p className="text-sm text-zinc-500">Real-time geospatial intelligence and routing.</p>
            <div className="flex items-center gap-4 mt-2">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold tracking-wide border border-blue-100">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                    Optimized using Hybrid GA-ACO
                </span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold tracking-wide border border-emerald-100">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    Predictive Routing Enabled
                </span>
            </div>
          </div>

          <div className="flex-1 flex gap-8 min-h-0 pb-2">
            <div className="w-80 flex flex-col gap-8 shrink-0 overflow-y-auto pr-1">
              <ControlPanel 
                processState={processState} 
                onTrigger={onTrigger} 
              />
              <InsightsPanel 
                processState={processState}
                nodes={nodes}
                metrics={metrics}
                activeRoute={activeRoute}
              />
            </div>

            <div className="flex-1 flex flex-col min-h-[500px]">
                <MapPanel 
                  route={activeRoute} 
                  baselineRoute={baselineRoute}
                  nodes={nodes}
                  baseLat={baseLat} 
                  baseLng={baseLng} 
                  isProcessing={processState === 'OPTIMIZING' || processState === 'PREDICTING'}
                  isComplete={processState === 'COMPLETED'}
                  selectedNode={selectedNode}
                  setSelectedNode={setSelectedNode}
                />
            </div>

            <NodeDetailsPanel 
                selectedNode={selectedNode}
                activeRoute={activeRoute}
                setSelectedNode={setSelectedNode}
            />
          </div>
      </div>
  );
}

export default OperationsView;
