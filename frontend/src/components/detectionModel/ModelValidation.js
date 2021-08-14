export function validate(bidirectionalNodes) {
    var validationMessages = []
    //check for cycles
    if (hasCycle(bidirectionalNodes)) {
        validationMessages.push({
            message: 'The graph must be acyclic',
            type: 'invalid',
        })
    }
    //unconnected nodes and detector presence
    var foundDetector = false
    var foundInput = false
    Object.keys(bidirectionalNodes).forEach(elemId => {
        const elem = bidirectionalNodes[elemId]
        if (elem.group !== 'input') {
            if (!elem.source || elem.source.length == 0) {
                validationMessages.push({
                    message: elem.display + ' (' + elem.id + '): no input nodes connected',
                    type: 'warning',
                })
            }
        }
        if (elem.group === 'detector') {
            foundDetector = true
        }
        if (elem.group === 'input') {
            foundInput = true
        }
    })
    if (!foundInput) validationMessages.push({message: 'No input node', type: 'warning'})
    if (!foundDetector) validationMessages.push({message: 'No detector node', type: 'warning'})
     
    return validationMessages
}


function hasCycle(bidirectionalNodes) {
    const nodes =  Object.keys(bidirectionalNodes)
    var adjList = {}
    nodes.forEach(elem => {
        adjList[elem] = []
    })
    nodes.forEach(elemId => {
        adjList[elemId] = [ ...bidirectionalNodes[elemId].target ]
    })
    const visited = {};
    const recStack = {}
    for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i]
    if (detectCycle(node, visited , recStack, adjList)) 
      return true  //cycle detected
    }
    return false
}

function detectCycle(vertex, visited, recStack, adjList) {
  if(!visited[vertex]){
    visited[vertex] = true;
    recStack[vertex] = true;
    const nodeNeighbors = adjList[vertex];
    for(let i = 0; i < nodeNeighbors.length; i++){
      const currentNode = nodeNeighbors[i];
      if(!visited[currentNode] && detectCycle(currentNode,visited, recStack, adjList)){
        return true;
      } else if (recStack[currentNode]){
        return true;
      }
    }
  }
  recStack[vertex] = false;
  return false;
}
