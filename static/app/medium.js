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
            {this.state.posts.map(item => <MediumFeedChild item={item} key={item} />)}
          </div>
        )
    }
}

function MediumFeedChild(props){
  return (
    <div key={props.item.url}>
      <br />
      <small>{props.item.url}</small>
      <br />
      <small>{props.item.title}</small>
      <br />
      <small>{props.item.preview}</small>
      <br />
      <small>{props.item.vote}</small>
    </div>
  )
}

ReactDOM.render(
  <MediumFeed />,
  document.getElementById('react')
);
