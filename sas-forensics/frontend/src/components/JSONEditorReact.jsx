import { useEffect, useRef } from 'react'
import { createJSONEditor, JSONEditorPropsOptional } from 'vanilla-jsoneditor'



const JSONEditorReact = (props) => {
    const { data, editable, onChange, ...otherprops} = props;
    const refContainer = useRef(null)
    const refEditor = useRef(null)

useEffect(() => {
    console.log(props)
    // create editor
    refEditor.current = createJSONEditor({
    target: refContainer.current,
    props: {
        data, editable, onChange, ...otherprops
    },
    });

    return () => {
    // destroy editor
    if (refEditor.current) {
        refEditor.current.destroy()
        refEditor.current = null
    }
    }
}, []);

// update props
useEffect(() => {
    if (refEditor.current) {
    refEditor.current.updateProps(props)
    }
}, [props]);

return <div ref={refContainer}></div>
}

export default JSONEditorReact