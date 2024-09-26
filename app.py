import streamlit as st
import json
import yaml
import outlines

# Load the schema.json file for datavzrd
with open("schema.json", "r") as f:
    schema = json.load(f)


# Function to generate the datavzrd config using Outlines
def generate_datavzrd_config(user_input, schema):
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
    print(json.dumps(schema))
    generator = outlines.generate.json(model, json.dumps(schema))
    print(user_input)
    config = generator(user_input)
    return config


# Streamlit app
def main():
    st.title("Datavzrd Config Generator")

    # Input box for user to provide natural language input
    user_input = st.text_area("Enter a description for the datavzrd config:",
                              "Create a config for sales dataset with views for regional and total sales.")

    # Button to generate the YAML configuration
    if st.button("Generate Config"):
        with st.spinner("Generating configuration..."):
            # Generate the config
            config_json = generate_datavzrd_config(user_input, schema)

            # Convert the JSON config to YAML
            config_yaml = yaml.safe_dump(config_json, sort_keys=False)

            # Display the generated YAML config
            st.subheader("Generated Datavzrd YAML Config:")
            st.code(config_yaml, language='yaml')

            # Option to download the YAML config
            st.download_button(
                label="Download YAML",
                data=config_yaml,
                file_name="datavzrd_config.yaml",
                mime="application/x-yaml"
            )


if __name__ == "__main__":
    main()
