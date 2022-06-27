import React, {useState} from 'react';
import Axios from 'axios';



function PostForm(props) {
    const url = "http://localhost:5000/"
    const [data, setData] = useState({
        prompt: "",
    })

    function handle(e) {
        const newData={...data}
        newData[e.target.id] = e.target.value
        setData(newData)
        console.log(newData)
    }


    function submit(e) {
        e.preventDefault();
        Axios.post(url,{
            prompt: data.prompt,
        })
        .then(res=> {
            console.log(res.data)
        })
    }

    return (
        <div>
            <form onSubmit={(e) => submit(e)}>
                <input onChange={(e)=>handle(e)} id= "prompt" value = {data.prompt} placeholder="prompt" type="text"></input>
                <button>submit</button>
            </form>
            
        </div>
    );
}

export default PostForm;