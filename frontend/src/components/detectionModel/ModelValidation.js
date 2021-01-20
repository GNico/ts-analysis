//medio feo refactorear despues 

function validate(bidirectionalNodes) {
    var validationMessages = []
    //chequear si tiene ciclos
    if (hasCycle(bidirectionalNodes)) {
        validationMessages.push({
            message: 'The graph must be acyclic',
            type: 'invalid',
            id: '',
        })
    }
    //buscar nodos sin conectar correctamente
    Object.keys(bidirectionalNodes).forEach(elemId => {
        const elem = bidirectionalNodes[elemId]
        if (elem.group == 'transformer') {
            if (!elem.target || elem.target.length == 0) {
                validationMessages.push({
                    message: 'Transformer output should be connected to a detector or another transformer',
                    type: 'warning',
                    id: elem.id,
                })
            }
        }
        if (elem.group == 'aggregator') {
            if (!elem.source || elem.source.length == 0) {                
                validationMessages.push({
                    message: 'Aggregator input should be a detector or another aggregator',
                    type: 'warning',
                    id: elem.id,
                })
            }         
        }
    })
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


export {
    validate,
}