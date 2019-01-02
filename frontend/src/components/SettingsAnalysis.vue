<template>
<div>
	<b-field label="Intervalo bucket">
		<input class="input" type="text" placeholder="ej: 30m" />
	</b-field>

	<b-field label="Config (temporario)">
		<textarea class="textarea" placeholder="ej: {parametro1: p1, otroparametro: op}"></textarea>
    </b-field>

	<div class="field is-grouped is-grouped-right">
      <p class="control">
        <a class="button is-primary" @click="$emit('analize')">
          Analizar
        </a>
      </p>
    </div>
</div>




</template>


<script>


export default {
	name: 'SettingsAnalysis',

}



</script>