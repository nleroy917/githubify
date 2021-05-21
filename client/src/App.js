import React from 'react';
import './styles.css';
import axios from 'axios';
import querystring from 'querystring';

const base_url =  'https://accounts.spotify.com/authorize?'
const payload = {
	client_id: process.env.REACT_APP_SPOTIFY_CLIENT_ID,
	response_type: 'code',
	scope: 'user-read-playback-state user-read-recently-played',
	redirect_uri: process.env.REACT_APP_SPOTIFY_REDIRECT_URI,
	show_dialog: true
}
const authorize_url = base_url + querystring.stringify(payload)

const App = () => {

  const [tokens, setTokens] = React.useState({})
  const [verifying, setVerifying] = React.useState(true)

  const fetchSettings = () => {
    let hdrs = {
      auth: process.env.REACT_APP_INTERNAL_TOKEN
    }
    axios.get(`/tokens`, {headers: hdrs})
    .then(res => {
      let tokens = res.data.tokens
      setVerifying(false)
      setTokens({
        accessToken: tokens.SPOTIFY_ACCESS_TOKEN,
        refreshToken: tokens.SPOTIFY_REFRESH_TOKEN
      })
    })
    .catch(err => {
      setVerifying(false)
    })
  }

  const sendTokensToServer = (tokens) => {
    let data = {
      access_token: tokens.accessToken,
      refresh_token: tokens.refreshToken
    }
    let hdrs = {
      auth: process.env.REACT_APP_INTERNAL_TOKEN,
    }
    axios.post(`/tokens`, {data: data}, {headers: hdrs})
    .then(res => {
      // pass
    })
  }

  const requestSpotifyTokens = (code) => {

    let hdrs = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + btoa(process.env.REACT_APP_SPOTIFY_CLIENT_ID + ':' + process.env.REACT_APP_SPOTIFY_CLIENT_SECRET)
    }

    let body = {
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: process.env.REACT_APP_SPOTIFY_REDIRECT_URI
    }

    axios.post(`https://accounts.spotify.com/api/token`, querystring.stringify(body),{headers: hdrs})
     .then(res => {
       let data = res.data
       setTokens({
         accessToken: data.access_token,
         refreshToken: data.refresh_token
       })
       sendTokensToServer({
        accessToken: data.access_token,
        refreshToken: data.refresh_token
      })
     })
     .catch(err => {
       fetchSettings()
     })
  }

  React.useEffect(()=>{
    let code = querystring.parse(window.location.href.slice(window.location.href.indexOf('?')+1)).code
    if(code !== undefined) {
      requestSpotifyTokens(code)
    } else {
      fetchSettings()
    }
  }, [])

  return (
    <div className="h-screen w-100 bg-green-300 flex flex-col justify-center items-center p-5">
      <p className="font-bold text-6xl my-5">githubify</p>
      <div className="text-center max-w-max lg:max-w-lg">
        <p>
          This web interface is to help you connect your Spotify account and get your access/refresh tokens in the database. This requires that you create an application with Spotify and do some minimal setup on Heroku. You can read more about that <a className="text-purple-700 underline" href="https://github.com/NLeRoy917/githubify">here</a>.
        </p>
      </div>
      <div className="flex flex-row my-5">
          {
            tokens.accessToken && tokens.refreshToken ?
            <button className="mx-2 bg-black border text-white border-black p-2 disabled:opacity-50 cursor-default" disabled={true}> 
              { 
                `Spotify connected!`
              }
            </button> 
            :
            <a href={authorize_url}>
              <button 
                className="mx-2 bg-black border text-white border-black p-2 hover:bg-transparent hover:text-black transition-all disabled:opacity-50"
                disabled={verifying}
              >
              { 
                verifying ?
                `verfying...` :
                `Connect Spotify`
              }
              </button>
            </a>
          }
        <a href="https://github.com/NLeRoy917/githubify">
          <button className="mx-2 bg-black border text-white border-black p-2 hover:bg-transparent hover:text-black transition-all">
            About
          </button>
        </a>
      </div>
      <div className="flex flex-col">
          {
            tokens.accessToken ? 
            <span className="text-lg"><span className="mx-1 text-lg">✅</span> Access token acquired!</span> :
            <span className="text-lg"><span className="mx-1 text-lg">❌</span> No access token.</span>
          }
          {
            tokens.refreshToken ? 
            <span className="text-lg"><span className="mx-1 text-lg">✅</span> Refresh token acquired!</span> :
            <span className="text-lg"><span className="mx-1 text-lg">❌</span> No refresh token.</span>
          }
      </div>
    </div>
  );
}

export default App;
