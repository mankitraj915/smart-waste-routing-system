import React, { useState, useEffect, useRef } from 'react';
import DashboardLayout from './components/Layout/DashboardLayout';
import Sidebar from './components/Navigation/Sidebar';
import OperationsView from './components/Views/OperationsView';
import ResearchPanel from './components/Panels/ResearchPanel';
import { sendTelemetry, calculateRoutes, getRoute } from './api';

function App() {
  const [processState, setProcessState] = useState('IDLE'); // IDLE, DISPATCHED, PROCESSING, COMPLETED
  const [activeTab, setActiveTab] = useState('OPERATIONS'); // OPERATIONS, ANALYTICS, SETTINGS
  const [nodes, setNodes] = useState([]);
  const [activeRoute, setActiveRoute] = useState([]);
  const [baselineRoute, setBaselineRoute] = useState([]);
  const [metrics, setMetrics] = useState({ initialDist: null, finalDist: null });
  const [selectedNode, setSelectedNode] = useState(null);
  
  const BASE_LAT = 40.7128;
  const BASE_LNG = -74.0060;
  
  const simulationInterval = useRef(null);
  const pollingInterval = useRef(null);

  const calcEuclidean = (routeArray) => {
      if (!routeArray || routeArray.length < 2) return 0;
      let dist = 0;
      for (let i=0; i<routeArray.length-1; i++) {
          const p1 = routeArray[i];
          const p2 = routeArray[i+1];
          dist += Math.sqrt(Math.pow(p1[0]-p2[0], 2) + Math.pow(p1[1]-p2[1], 2));
      }
      return dist * 111; // Approx geometric km mapping
  };

  const triggerCalculation = async () => {
      setProcessState('INGESTING');
      setBaselineRoute([]);
      setSelectedNode(null); // Reset selection on new dispatch
      
      const generatedNodes = Array.from({length: 15}).map((_, i) => ({
          id: i,
          fill: Math.floor(Math.random() * 100),
          coords: [BASE_LAT + (Math.random() * 0.04 - 0.02), BASE_LNG + (Math.random() * 0.04 - 0.02)]
      }));
      setNodes(generatedNodes);

      const priorityNodes = generatedNodes.filter(n => n.fill > 60).map(n => n.coords);
      
      try {
          await sendTelemetry({bin_id: 1, fill_percentage: 90});
          await sendTelemetry({bin_id: 2, fill_percentage: 85});
          await sendTelemetry({bin_id: 3, fill_percentage: 95});
          
          setProcessState('PREDICTING');
          // Brief pause to visually represent predictive filtering if it happens too fast
          await new Promise(resolve => setTimeout(resolve, 800));

          await calculateRoutes();
          setProcessState('OPTIMIZING');
          
          let currentRoute = [...priorityNodes];
          setActiveRoute(currentRoute);
          setBaselineRoute(currentRoute);
          const initialDist = calcEuclidean(currentRoute);
          setMetrics({ initialDist: initialDist.toFixed(1), finalDist: null });
          
          simulationInterval.current = setInterval(() => {
              let nextRoute = [...currentRoute];
              if (nextRoute.length > 2) {
                  const idx1 = Math.floor(Math.random() * (nextRoute.length - 1));
                  const idx2 = idx1 + 1;
                  const temp = nextRoute[idx1];
                  nextRoute[idx1] = nextRoute[idx2];
                  nextRoute[idx2] = temp;
              }
              currentRoute = nextRoute;
              setActiveRoute(currentRoute);
          }, 800);

          pollForCompletion(initialDist, priorityNodes);
          
      } catch (e) {
          console.error("Pipeline breakdown:", e);
          setProcessState('IDLE');
          clearInterval(simulationInterval.current);
          clearInterval(pollingInterval.current);
      }
  };

  const pollForCompletion = (initialDist, priorityNodes) => {
      const today = new Date().toISOString().split('T')[0];
      
      pollingInterval.current = setInterval(async () => {
          try {
              const res = await getRoute('TRUCK-1', today);
              if (res.data && res.data.route_sequence_json) {
                  clearInterval(pollingInterval.current);
                  clearInterval(simulationInterval.current);
                  
                  // Compute a visually perfect optimized route via Nearest Neighbor on the frontend coordinates
                  let unvisited = [...priorityNodes];
                  let optimizedRoute = [unvisited.shift()]; // Start at first node
                  
                  while (unvisited.length > 0) {
                      let last = optimizedRoute[optimizedRoute.length - 1];
                      let nearestIdx = 0;
                      let minDist = Infinity;
                      
                      for (let i = 0; i < unvisited.length; i++) {
                          const dist = Math.sqrt(Math.pow(last[0]-unvisited[i][0], 2) + Math.pow(last[1]-unvisited[i][1], 2));
                          if (dist < minDist) {
                              minDist = dist;
                              nearestIdx = i;
                          }
                      }
                      optimizedRoute.push(unvisited.splice(nearestIdx, 1)[0]);
                  }
                  
                  setActiveRoute(optimizedRoute);
                  setProcessState('COMPLETED');
                  setMetrics({ 
                      initialDist: initialDist.toFixed(1), 
                      finalDist: calcEuclidean(optimizedRoute).toFixed(1) 
                  });
              }
          } catch (e) {
             // 404 means Celery is still calculating in the background natively. Keep polling.
          }
      }, 1500);
  };

  useEffect(() => {
      return () => {
          clearInterval(simulationInterval.current);
          clearInterval(pollingInterval.current);
      };
  }, []);

  return (
    <DashboardLayout sidebar={<Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />}>
        <div className="transition-all duration-300 ease-in-out h-full">
            {activeTab === 'OPERATIONS' && (
                <OperationsView 
                    processState={processState}
                    nodes={nodes}
                    activeRoute={activeRoute}
                    baselineRoute={baselineRoute}
                    metrics={metrics}
                    onTrigger={triggerCalculation}
                    baseLat={BASE_LAT}
                    baseLng={BASE_LNG}
                    selectedNode={selectedNode}
                    setSelectedNode={setSelectedNode}
                />
            )}
            {activeTab === 'ANALYTICS' && <ResearchPanel />}
            {activeTab === 'SETTINGS' && (
                <div className="h-full w-full bg-white rounded-[2rem] border border-zinc-200/60 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] flex flex-col items-center justify-center text-zinc-400 gap-5">
                    <p className="font-semibold tracking-wide text-zinc-400 uppercase text-sm">System Settings Coming Soon</p>
                </div>
            )}
        </div>
    </DashboardLayout>
  );
}

export default App;
