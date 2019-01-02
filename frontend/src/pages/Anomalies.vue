<template>



    
 <div class="columns">
    <div class="column is-one-fifth">

          <!--  <section class="message">
            <div class="message-header">
              <p>alalah</p>
            </div>
            <div class="message-body">
              <p>button ?</p>
              <b-dropdown hoverable>
                  <button class="button is-primary" slot="trigger">
                      <span>Click me!</span>
                  </button>

                  <b-dropdown-item>Action</b-dropdown-item>
                  <b-dropdown-item>Another action</b-dropdown-item>
                  <b-dropdown-item>Something else</b-dropdown-item>
              </b-dropdown>
            </div>
          </section>  -->
             <nav class="panel">
            
              <p class="panel-tabs">
                <a class="is-active">Visualize</a>
                <a>Analize</a>
                <a>Compare</a>
              </p>
              <div class="panel-block">
                <div class="control">
                  <label class="label">Context</label>
                  <input class="input" type="text" placeholder="Text input">
                </div>
              </div>
              <div class="panel-block">
                <div class="control">
                  <label class="label">Tag</label>
                  <input class="input" type="text" placeholder="Text input">
                </div>
              </div>
              <a class="panel-block">
                <span class="panel-icon">
                  <i class="fas fa-book" aria-hidden="true"></i>
                </span>
                jgthms.github.io
              </a>
              <a class="panel-block">
                <span class="panel-icon">
                  <i class="fas fa-code-branch" aria-hidden="true"></i>
                </span>
                daniellowtw/infboard
              </a>
              <a class="panel-block">
                <span class="panel-icon">
                  <i class="fas fa-code-branch" aria-hidden="true"></i>
                </span>
                mojs
              </a>
              <label class="panel-block">
                <input type="checkbox">
                remember me
              </label>
              <div class="panel-block">
                <button class="button is-link is-outlined is-fullwidth">
                  reset all filters
                </button>
              </div>
            </nav> 
    </div>

    <div class="column is-one-fifth is-offset-4">
        <div class="tabs is-toggle is-medium is-fullwidth">
            <ul>
            <li class="is-active">
              <a>
                <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
                <span>Visualize</span>
              </a>
            </li>
            <li>
              <a>
                <span class="icon is-small"><i class="fas fa-music" aria-hidden="true"></i></span>
                <span>Analize</span>
              </a>
            </li>
            <li>
              <a>
                <span class="icon is-small"><i class="fas fa-film" aria-hidden="true"></i></span>
                <span>Compare</span>
              </a>
            </li>
            </ul>
        </div>
    </div>

</div> 

</template>


<script>

export default {
    
}

</script>

