import React from 'react'
import ReactDOM from 'react-dom'


class MediumFeed extends React.Component {
    constructor(props){
      super(props)
      this.state = {posts: []}
      const prefix = window.prefix
      const posts = []
      fetch('/feeds/medium/'+prefix).then(data => {
        data.json().then(data => {
          data.data.forEach(item => {
            this.setState({
              posts: [...this.state.posts, item]
            })
          })
        })
      }).catch(err => {
        console.log(err)
      })
    }
    render () {
      console.log(this.state.posts)
        return(
          <div>
            <a href="#" className='link-feed uk-position-medium uk-position-top-center'>Open on Medium</a>
            <div className='medium-grid uk-position-center'>
              {this.state.posts.map(item => <MediumFeedChild item={item} key={item.url} />)}
            </div>
          </div>
        )
    }
}

function MediumFeedChild(props){
  return (
    <div className="card">
      <h3><a className="medium-anchor" href={props.item.url} target='_blank'>{props.item.title}</a></h3>
      <p className="preview">{props.item.preview}</p>
      <small>{props.item.vote}</small>
    </div>
  )
}

ReactDOM.render(
  <MediumFeed />,
  document.getElementById('react-medium')
);
