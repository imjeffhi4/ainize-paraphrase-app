<script>
    //Input values
    let inputText = ""
    let paraphraseText = ""
    let wordCountChange = 1 // 1 attempts to reduce number of words, 3 attempts to increase number of words
    let changeDistance = 3 // 1 tells the model to produce small changes in terms of structure, 4 tells the model to produce large changes. 

    //Metrics returned from API call
    let similarity = 0
    let editDistance = 0

    // Number of words to display to user
    $: originalWordCount = inputText.split(" ").length
    $: paraphraseWordCount = paraphraseText.split(" ").length

    async function getGeneratedParaphrase() {
        paraphraseText = ""
        //Ainize deployment host. If running locally, change to localhost:8000
        const res = await fetch("https://finished-ainize-paraphrase-app-imjeffhi4.endpoint.ainize.ai/paraphrase/", {
            method: "POST",
            body: JSON.stringify({
                text: inputText,
                distance: changeDistance,
                wordCount: wordCountChange,
            }),
        })
        const json = await res.json()

        //Storing response in variables
        paraphraseText = json["Paraphrase"]
        similarity = json["Similarity"]
        editDistance = json["distance"]
    }
</script>

<main class="paraphrase">
    <article class="io paraphrase_form">
        <textarea
            placeholder="Enter text that you'd like to paraphrase"
            class="user_text"
            bind:value={inputText}
        />
        <div class="sliders">
            <div>
                <p>Small or Large changes?</p>
                <article class="slide">
                    <span>Small</span>
                    <input type="range" min="1" max="4" bind:value={changeDistance} />
                    <span>Large</span>
                </article>
            </div>
            <div>
                <p>Reduce or expand word count?</p>
                <article class="slide">
                    <span>Reduce</span>
                    <input type="range" min="1" max="3" bind:value={wordCountChange}/>
                    <span>Expand</span>
                </article>
            </div>
        </div>
        <div class="btnContainer">
            <button class="btn" on:click={getGeneratedParaphrase} >Paraphrase</button>
        </div>
        <div class="results">
            <span>Word Count: {originalWordCount}</span>
        </div>
    </article>
    <article class="io output">
        <p>{paraphraseText}</p>
        {#if similarity}
            <div class="results">
                <span>Similarity: {similarity}</span>
                <span>Distance: {editDistance}</span>
                <span>Word Count: {paraphraseWordCount}</span>
            </div>
        {/if}
    </article>
</main>

<style>
    .paraphrase {
        display: flex;
        justify-content: center;
        margin-top: 4px;
        padding: 10px;
    }
    .io {
        width: 600px;
        height: 500px;
        border: 2px white solid;
        margin: 5px;
        position: relative;
    }
    .user_text {
        height: 500px;
        width: 100%;
        padding: 0.4em 0.4em 0.4em 0;
    }
    input {
        padding: 0px;
        margin: 0px;
    }
    .slide {
        display: flex;
        justify-content: center;
        flex-direction: row;
        padding: 10px 0;
    }
    .sliders {
        display: flex;
        justify-content: center;
    }
    .sliders div {
        margin: 5px 20px;
        padding: 5 10px;
        text-align: center;
    }
    .btn {
        padding: 10px;
        border-radius: 5px;
    }
    .btnContainer {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .results {
        position: absolute;
        bottom: 0;
    }
    span {
        margin: 1px 10px;
    }
    p {
        padding: 0px;
        margin: 2px;
    }
</style>
