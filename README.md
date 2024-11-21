# ✨ Predicting Star Type using Artificial Intelligence 
This <a href="https://startypepredictor.streamlit.app/" target="_blank">web application</a>allows you to do the following:-
1. Predict type of a single star using single prediction mode.
2. Predict type of multiple stars using bulk prediction mode.

<img src="media/final-video.gif" alt="Web App GIF" width=90%>

## ⚙️ How to Set Up This Project in Your System
1. Clone this repository using the web URL given below or download the ZIP file.
   ```bash
   git clone https://github.com/SpartificialUdemy/project_2.git
   ```

2. Create the virtual environment in your system:
   - **Windows**
   ```bash
   python -m venv venv
   ```
   - **Linux or Mac**
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**
   ```bash
   venv\Scripts\activate
   ```
   - **Linux or Mac**
   ```bash
   source venv/bin/activate
   ```

4. Install the requirements:
   - **Windows**
   ```bash
   python -m pip install -r requirements.txt
   ```
   - **Linux or Mac**
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend powered by FastAPI using Uvicorn:
   ```bash
   uvicorn backend:app 
   ```

6. Run the frontend powered by Streamlit:
   ```bash
   streamlit run frontend.py
   ```

## 🔧 Tools used in This Project
1. **FastAPI** - To build the API endpoints
2. **Streamlit** - To build and host the frontend of the web application
3. **Render** - To host the backend API built using FastAPI
4. **Scikit-Learn** - To build the dataset pipeline, train the model, and evaluate it
5. **Matplotlib** - To visualize the cost vs iterations and in the web application to visualize the regression line
6. **Pandas** - To read CSV files, create the dataframe, and save dataframes back to CSV

## 💖 Acknowledgments
- Special thanks to the authors of the libraries used in this project.
  
## 📧 Contact
For questions or support, please reach out to me [via email](https://mail.google.com/mail/?view=cm&fs=1&to=rohan.calculus@gmail.com).
