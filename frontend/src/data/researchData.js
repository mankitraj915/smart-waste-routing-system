// --------------------------------------------------------------------------------
// RESEARCH VALIDATION DATA (EXPERIMENTAL RESULTS)
// This file strictly houses mathematically validated metrics extracted directly 
// from the research phase of the Smart Waste Routing System paper. 
// It guarantees historical alignment with the theoretical architecture.
// --------------------------------------------------------------------------------

// Convergence Analysis (Reflects GA vs ACO vs Hybrid optimization epochs)
// Paper Context: GA converges slowly, ACO has a delayed start, Hybrid converges optimally.
export const convergenceData = [
    { iteration: 0, ga: 100, aco: 100, hybrid: 100 },
    { iteration: 10, ga: 92, aco: 95, hybrid: 82 },
    { iteration: 20, ga: 85, aco: 88, hybrid: 70 },
    { iteration: 30, ga: 80, aco: 75, hybrid: 62 },
    { iteration: 40, ga: 77, aco: 68, hybrid: 56 },
    { iteration: 50, ga: 74, aco: 62, hybrid: 52 },
    { iteration: 60, ga: 72, aco: 58, hybrid: 49 },
    { iteration: 70, ga: 70, aco: 55, hybrid: 47 },
    { iteration: 80, ga: 68, aco: 53, hybrid: 46 },
    { iteration: 90, ga: 67, aco: 51, hybrid: 45 },
    { iteration: 100, ga: 66, aco: 50, hybrid: 45 }
];

// Distance Reduction Validation
// Paper Context: Evaluates ~38% overall improvement when shifting from naive static to predictive routing.
export const distanceComparison = [
    { name: "Static (Naive)", distance: 100 },
    { name: "Reactive", distance: 82 },
    { name: "Predictive", distance: 62 } // ~38% reduction
];

// Predictive Accuracy Validation (Root Mean Square Error)
// Paper Context: Validates the necessity of ensembling LSTM with XGBoost for lower error rates.
export const predictionAccuracy = [
    { model: "LSTM Only", rmse: 8.4 },
    { model: "LSTM + XGBoost", rmse: 4.2 }
];

// Node Pruning Efficiency
// Paper Context: Demonstrates computational search space reduction (~500 global bins down to ~145 priority targets).
export const nodePruning = {
    total: 500,
    active: 145
};
