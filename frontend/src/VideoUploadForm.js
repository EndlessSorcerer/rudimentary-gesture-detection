import React, { useState } from 'react';
import axios from 'axios';
import ReactPlayer from 'react-player';

const VideoUploadForm = () => {
    const [title, setTitle] = useState('');
    const [videoFile, setVideoFile] = useState(null);
    const [processedResult, setProcessedResult] = useState('');

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
    };

    const handleVideoFileChange = (e) => {
        setVideoFile(e.target.files[0]);
    };
    console.log('0');
    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('title', title);
        formData.append('video_file', videoFile);
        console.log('0');
        try {
            console.log('0');
            const response = await axios.post('http://127.0.0.1:8000/api/videos/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log('1');
            const processedResult = response.data.processed_result;

            console.log('Uploaded video:', response.data);
            console.log('Processed result:', processedResult);
            setTitle('');
            setVideoFile(null);
            setProcessedResult(processedResult);
        } catch (error) {
            console.error('Error uploading video:', error);
        }
    };

    return (
        <div>
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="title">Title:</label>
                <input type="text" id="title" value={title} onChange={handleTitleChange} />
            </div>
            <div>
                <label htmlFor="videoFile">Video File:</label>
                <input type="file" id="videoFile" onChange={handleVideoFileChange} />
            </div>
            <button type="submit">Upload</button>
        </form>
        {/* {processedResult && ( */}
                <div>
                    {/* <ReactPlayer url={processedResult} controls={true}/> */}
                    {/* <video width="750" height="500" controls >
      <source src="http://127.0.0.1:8000/processed/output.mp4" type="file"/>
     </video> */}
                </div>
            {/* ) */}
            {/* } */}
        </div>
    );
};

export default VideoUploadForm;
