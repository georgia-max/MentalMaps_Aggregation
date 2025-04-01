const graph = {
    nodes: [
        { id: 'Population', label: 'Population' },
        { id: 'Industrial Output', label: 'Industrial Output' },
        { id: 'Capital Investment', label: 'Capital Investment' },
        { id: 'Resource Depletion', label: 'Resource Depletion' },
        { id: 'Pollution', label: 'Pollution' }
    ],
    edges: [
        { source: 'Population', target: 'Industrial Output', type: 'positive' },
        { source: 'Industrial Output', target: 'Capital Investment', type: 'positive' },
        { source: 'Capital Investment', target: 'Industrial Output', type: 'positive' },
        { source: 'Industrial Output', target: 'Resource Depletion', type: 'positive' },
        { source: 'Industrial Output', target: 'Pollution', type: 'positive' },
        { source: 'Resource Depletion', target: 'Industrial Output', type: 'negative' },
        { source: 'Resource Depletion', target: 'Population', type: 'negative' },
        { source: 'Pollution', target: 'Industrial Output', type: 'negative' },
        { source: 'Pollution', target: 'Population', type: 'negative' }
    ]
};

function generateGraphData() {
    return graph;
}

const graphData = generateGraphData();
console.log(JSON.stringify(graphData, null, 2));