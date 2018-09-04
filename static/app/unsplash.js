import React from 'react'
import ReactDOM from 'react-dom'


class UnsplashFeed extends React.Component {
  constructor(props){
    super(props)
    this.state = {images: []}
    const prefix = window.prefix
    const posts = []
    fetch('/feeds/unsplash/'+prefix).then(data => {
      data.json().then(data => {
        data.data.forEach(item => {
          this.setState({
            images: [...this.state.images, item]
          })
        })
      })
    }).catch(err => {
      console.log(err)
    })
  }
  render () {
    return(
      <div>
        <a href="#" className='link-feed uk-position-medium uk-position-top-center'>View on Unsplash</a>
        <div className='medium-grid uk-position-center'>
          {this.state.images.map(item => <UnsplashFeedChild url={item} key={item} />)}
        </div>
      </div>
    )
  }
}

function UnsplashFeedChild(props){
  return (
    <img src={props.url} className='image-card' />
  )
}

ReactDOM.render(
  <UnsplashFeed />,
  document.getElementById('react-unsplash')
);
