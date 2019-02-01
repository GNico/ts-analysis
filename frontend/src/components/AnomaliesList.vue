<template>

  <b-table 
    :data="anomalies" 
    :columns="columns" 
    hoverable
    checkable
  />

</template>


<script>


export default {
  data() {
    return {
      anomalies: [
        { 'color': 1, 'score': 50, 'start_date': '2016-10-15 13:43:27', 'end_date': '2016-10-15 13:43:27', 'duration': 'Male' },
        { 'color': 2, 'score': 70,  'start_date': '2016-12-15 06:00:53', 'end_date': '2016-12-15 06:00:53', 'duration': 'Male' },
        { 'color': 3, 'score': 20, 'start_date': '2016-04-26 06:26:28', 'end_date': '2016-04-26 06:26:28', 'duration': 'Female' },
        { 'color': 4, 'score': 25, 'start_date': '2016-04-10 10:28:46','end_date': '2016-04-10 10:28:46', 'duration': 'Male' },
        { 'color': 5, 'score': 36, 'start_date': '2016-12-06 14:38:38', 'end_date': '2016-12-06 14:38:38', 'duration': 'Female' }
      ],
      columns: [
        {
            field: 'color',
            label: 'Color',
        },
        {
            field: 'score',
            label: 'Score',
        },
        {
            field: 'start_date',
            label: 'Start date',
            centered: true
        },
        {
            field: 'end_date',
            label: 'End date',
            centered: true
        },
        {
            field: 'duration',
            label: 'Duration',
        }
      ]
    }
  }
}


</script>