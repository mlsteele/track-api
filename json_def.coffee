schema =
    event_name: "Found stray dog"
    data:
        color:
            doc: "Color of the dog."
        feet:
            number:
                doc: "Number of feet"
            wear:
                doc: "Wear on dog."
            nail_length:
                docs: "Length of toenails."
                optional: yes
            notes:
                doc: "Extra notes."
                optional: yes
                disable_schema: yes
    context:
        username: {}
        session_id: {}
        callsite: {}


console.log JSON.stringify schema, null, 2
