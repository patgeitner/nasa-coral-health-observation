import streamlit as st

def resetSession():
	for key in st.session_state.keys():
		del st.session_state[key]
resetSession()

st.set_page_config(page_title = "GOTECH",
				   page_icon = "🏡")

st.markdown(
		"""
		<style>
		.img{
			width:50px;
			height:50px;
		}
		</style>
		""",
		unsafe_allow_html=True
	)

st.markdown("<h1 style='text-align: center; color: white;'> \
					Geophysical Observations Toolkit for Evaluating Coral Health (GOTECH) \
					<img class='img' src='https://seeklogo.com/images/N/nasa-logo-D8FA7F7DE9-seeklogo.com.png'/> \
				</h1>", unsafe_allow_html=True)
	
st.markdown("<h2 style='text-align: center; color: white;'> \
					University of Rochester Capstone Fall 2022 \
				</h2>", unsafe_allow_html=True)
	
st.markdown("<p style='text-align: center; color: white;'> \
					Lisa Pink, Matthew Johnson, Mohamad Ali Kalassina, Patrick Geitner, Thomas Durkin \
				</p>", unsafe_allow_html=True)
	
st.markdown("""---""")

st.markdown("<p style='text-align: center; color: white;'> \
					A dashboard to predict whether a given point is coral or not. \
					Bleaching severity level will be displayed for points that are predicted as coral. \
				</p>", unsafe_allow_html=True)