<template>
<div>
	<b-field label="Intervalo bucket">
		<input class="input" type="text" placeholder="ej: 30m" />
	</b-field>

	<b-field label="Config (temporario)">
		<textarea class="textarea" placeholder="ej: {parametro1: p1, otroparametro: op}"></textarea>
    </b-field>

	<div class="box has-text-centered">
        <a class="button is-primary is-medium" @click="$emit('analize')">
          Analizar
        </a>
    </div>
</div>




</template>


<script>


export default {
	name: 'SettingsAnalysis',

}



</script>