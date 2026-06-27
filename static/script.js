// ======================================
// ELEMENT
// ======================================

const chatBox = document.getElementById("chat-box");

const input = document.getElementById("question");

const sendBtn = document.getElementById("send-btn");


// ======================================
// SCROLL
// ======================================

function scrollBottom(){

    requestAnimationFrame(()=>{

        chatBox.scrollTop = chatBox.scrollHeight;

    });

}


// ======================================
// ESCAPE HTML
// ======================================

function escapeHtml(text){

    return text

    .replace(/&/g,"&amp;")

    .replace(/</g,"&lt;")

    .replace(/>/g,"&gt;");

}


// ======================================
// ADD USER MESSAGE
// ======================================

function addUserMessage(text){

    const div=document.createElement("div");

    div.className="message user";

    div.innerHTML=`

        <div class="bubble">

            ${escapeHtml(text)}

        </div>

    `;

    chatBox.appendChild(div);

    scrollBottom();

}


// ======================================
// ADD BOT MESSAGE
// ======================================

function addBotMessage(html){

    const div=document.createElement("div");

    div.className="message bot";

    div.innerHTML=`

        <div class="bubble">

            ${html}

        </div>

    `;

    chatBox.appendChild(div);

    scrollBottom();

}


// ======================================
// LOADING
// ======================================

function addLoading(){

    const div=document.createElement("div");

    div.className="message bot loading";

    div.id="loading";

    div.innerHTML=`

        <div class="bubble">

            🤖 Sedang berpikir...

        </div>

    `;

    chatBox.appendChild(div);

    scrollBottom();

}


function removeLoading(){

    const loading=document.getElementById("loading");

    if(loading){

        loading.remove();

    }

}


// ======================================
// SEND MESSAGE
// ======================================

async function sendMessage(){

    const question=input.value.trim();

    if(question==="") return;

    addUserMessage(question);

    input.value="";

    input.disabled=true;

    sendBtn.disabled=true;

    addLoading();

    try{

        const response=await fetch(

            "/chat",

            {

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify({

                    question:question

                })

            }

        );

        const data=await response.json();

        removeLoading();

        window.lastAnswer=data;

        renderAnswer(data);

    }

    catch(e){

        removeLoading();

        addBotMessage(

            "<span style='color:red'>❌ Server Error</span>"

        );

        console.error(e);

    }

    input.disabled=false;

    sendBtn.disabled=false;

    input.focus();

}
// ======================================
// BUTTON
// ======================================

sendBtn.addEventListener(

    "click",

    sendMessage

);


// ======================================
// ENTER
// ======================================

input.addEventListener(

    "keydown",

    function(e){

        if(e.key==="Enter"){

            e.preventDefault();

            sendMessage();

        }

    }

);


// ======================================
// AUTO FOCUS
// ======================================

window.onload=function(){

    input.focus();

};

// ======================================
// RENDER ANSWER
// ======================================

function renderAnswer(data){

    let html = `

        <div>

            ${data.answer.replace(/\n/g,"<br>")}

        </div>

    `;

    if(data.sources && data.sources.length>0){

        html += `

        <div class="sources">

            <h4>📄 Sources</h4>

        `;

        data.sources.forEach(src=>{

            html += `

            <div class="source-card">

                <b>${src.document}</b>

                <br>

                📄 Page ${src.page}

                <br>

                Similarity :
                ${Number(src.score).toFixed(4)}

                ${src.rerank_score !== undefined ?

                `<br>Rerank :
                ${Number(src.rerank_score).toFixed(4)}`

                : ""}

            </div>

            `;

        });

        html += "</div>";

    }

    addBotMessage(html);

}


// ======================================
// LOAD DOCUMENT
// ======================================

async function loadDocuments(){

    try{

        const response = await fetch("/documents");

        const docs = await response.json();

        const container = document.getElementById("doc-list");

        container.innerHTML="";

        docs.forEach(doc=>{

            container.innerHTML += `

            <div class="doc-card">

                <div class="doc-title">

                    📄 ${doc.document}

                </div>

                <div class="doc-info">

                    ${doc.pages} Pages

                    <br>

                    ${doc.chunks} Chunks

                </div>

            </div>

            `;

        });

    }

    catch(e){

        console.log(e);

    }

}


// ======================================
// LOAD STATS
// ======================================

async function loadStats(){

    try{

        const response = await fetch("/stats");

        const stats = await response.json();

        document.getElementById("stats").innerHTML=`

            <b>Documents</b>

            <br>

            ${stats.documents}

            <hr>

            <b>Pages</b>

            <br>

            ${stats.pages}

            <hr>

            <b>Chunks</b>

            <br>

            ${stats.chunks}

        `;

    }

    catch(e){

        console.log(e);

    }

}


// ======================================
// UPLOAD
// ======================================

async function uploadPDF(){

    const file=document.getElementById("pdf").files[0];

    if(!file){

        alert("Pilih PDF terlebih dahulu.");

        return;

    }

    const form=new FormData();

    form.append(

        "file",

        file

    );

    const btn=document.getElementById("upload-btn");

    btn.disabled=true;

    btn.innerHTML="Uploading...";

    try{

        const response=await fetch(

            "/upload",

            {

                method:"POST",

                body:form

            }

        );

        const result=await response.json();

        btn.innerHTML="Upload PDF";

        btn.disabled=false;

        document.getElementById("pdf").value="";

        await loadDocuments();

        await loadStats();

        alert(

            `✅ Upload Berhasil

Pages : ${result.pages}

Chunks : ${result.chunks}`

        );

    }

    catch(e){

        btn.innerHTML="Upload PDF";

        btn.disabled=false;

        alert("Upload gagal.");

        console.log(e);

    }

}
// ======================================
// EMPTY CHAT
// ======================================

function showWelcome(){

    if(chatBox.children.length!==0) return;

    chatBox.innerHTML=`

        <div class="empty-chat">

            <h2>

                🤖

            </h2>

            <h3>

                AI Document Assistant

            </h3>

            <p>

                Upload PDF kemudian tanyakan apa saja.

            </p>

        </div>

    `;

}

function removeWelcome(){

    const empty=document.querySelector(".empty-chat");

    if(empty){

        empty.remove();

    }

}


// ======================================
// OVERRIDE MESSAGE
// ======================================

const oldUser=addUserMessage;

addUserMessage=function(text){

    removeWelcome();

    oldUser(text);

}

const oldBot=addBotMessage;

addBotMessage=function(text){

    removeWelcome();

    oldBot(text);

}


// ======================================
// DRAG DROP
// ======================================

const uploadBox=document.querySelector(".upload-box");

uploadBox.addEventListener(

    "dragover",

    function(e){

        e.preventDefault();

        uploadBox.classList.add("drag");

    }

);

uploadBox.addEventListener(

    "dragleave",

    function(){

        uploadBox.classList.remove("drag");

    }

);

uploadBox.addEventListener(

    "drop",

    function(e){

        e.preventDefault();

        uploadBox.classList.remove("drag");

        document.getElementById("pdf").files=e.dataTransfer.files;

    }

);


// ======================================
// BUTTON LOADING
// ======================================

function buttonLoading(status){

    if(status){

        sendBtn.disabled=true;

        sendBtn.innerHTML="...";

    }

    else{

        sendBtn.disabled=false;

        sendBtn.innerHTML="Send";

    }

}


// ======================================
// PATCH SENDMESSAGE
// ======================================

const oldSend=sendMessage;

sendMessage=async function(){

    buttonLoading(true);

    await oldSend();

    buttonLoading(false);

}


// ======================================
// AUTO RESIZE
// ======================================

window.addEventListener(

    "resize",

    scrollBottom

);


// ======================================
// AUTO REFRESH DOC
// ======================================

setInterval(

    loadDocuments,

    10000

);


// ======================================
// AUTO REFRESH STATS
// ======================================

setInterval(

    loadStats,

    10000

);


// ======================================
// START
// ======================================

window.addEventListener(

    "load",

    ()=>{

        showWelcome();

        scrollBottom();

    }

);