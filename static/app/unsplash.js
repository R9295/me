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
            {this.state.images.map(item => <UnsplashFeedChild url={item} key={item} />)}
          </div>
        )
    }
}

function UnsplashFeedChild(props){
  return (
    <div key={props.url}>
      <small>{props.url}</small>
    </div>
  )
}

ReactDOM.render(
  <UnsplashFeed />,
  document.getElementById('react')
);
