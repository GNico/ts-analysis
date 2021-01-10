<template>
<div>
  <Tree 
    :value="treeData"
    indent="50"
    draggingNodePositionMode='top_left_corner'>
    <span slot-scope="{node, index, path, tree}">
      <PipeNode :title="path.join('.')"/>
    </span>
  </Tree>

</div>
</template>


<script>
import 'he-tree-vue/dist/he-tree-vue.css';
import {Tree, Draggable} from 'he-tree-vue';

import PipeNode from './PipeNode';


export default {
  components: { PipeNode, Tree: Tree.mixPlugins([Draggable]) },
  data() {
    return {
      treeData: [
        {title: 'node 1'}, 
        {title: 'node 3'},
        {title: 'node 4'},
        {title: 'node 2', 
        children: [
          {title: 'node 2-1'},
          {title: 'node 2-2'}
        ]}
      ]
    }
  },
}


/*
<b>{{index}}</b>
      Title: {{node.title}}
      - path: <i>{{path.join(',')}}</i>
      */
</script>