################# Define custom functions w/in Python ################
import os
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def get_signals_status(status):
    # Fixed desired keys with their new names
    key_mappings = {
        'kode': 'ticker',
        'plantp1': 'take-profit-1',
        'plantp2': 'take-profit-2',
        'plancl': 'cut-loss-1',
        'plancl2': 'cut-loss-2',
        'planskenario': 'scenario'
    }
    
    url = "https://sucor.sahamology.id/signal"
    payload = {
        'id': st.secrets["id"],
        'key': st.secrets["key"],
        'short': 'volume',
        'status': status
    }
    headers = {}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            json_response = response.json()
            signals = json_response.get("signal", [])
            if signals:
                # Get up to the first three signals from the list
                first_three_signals = signals[:3]
                # Process each of the first three signals
                processed_signals = [
                    {new_key: signal.get(old_key, None) for old_key, new_key in key_mappings.items()}
                    for signal in first_three_signals
                ]
                return processed_signals
            else:
                return "No signals found"
        except ValueError:  # JSONDecodeError in Python 3.5+
            return "Error decoding JSON response"
    else:
        return f"API request failed with status code: {response.status_code}"
    

# Example usage
# status = "fresh buy"
# first_signal_filtered_and_renamed = get_first_signal_for_status(status)
# print(f"Filtered and renamed first signal for status '{status}':", first_signal_filtered_and_renamed)

# print(get_first_signal_for_status("fresh buy"))


def get_trading_info(ticker):
    url = "https://sucor.sahamology.id/arvita/artificial"
    payload = {
        'id': st.secrets["id"],
        'key': st.secrets["key"],
        'pesan': '#'+ticker  # Ensure this is the correct key for the ticker
    }
    headers = {}
    
    response = requests.post(url, headers=headers, data=payload)

    # print(f"HTTP Status Code: {response.status_code}")  # Debugging line

    if response.status_code == 200:
        try:
            json_response = response.json()
        #    print(f"JSON Response: {json_response}")  # Debugging line

            result = json_response.get("result", "No signals found")
            return result
        except ValueError as e:  # More specific exception handling
            print(f"Error decoding JSON: {e}")  # Debugging line
            return "Error decoding JSON response"
    else:
        return f"API request failed with status code: {response.status_code}"
    

def get_invest_info(ticker):
    url = "https://sucor.sahamology.id/arvita/artificial"
    payload = {
        'id': st.secrets["id"],
        'key': st.secrets["key"],
        'pesan': 'invest #'+ticker  # Ensure this is the correct key for the ticker
    }
    headers = {}
    
    response = requests.post(url, headers=headers, data=payload)

    # print(f"HTTP Status Code: {response.status_code}")  # Debugging line

    if response.status_code == 200:
        try:
            json_response = response.json()
        #    print(f"JSON Response: {json_response}")  # Debugging line

            result = json_response.get("result", "No signals found")
            return result
        except ValueError as e:  # More specific exception handling
            print(f"Error decoding JSON: {e}")  # Debugging line
            return "Error decoding JSON response"
    else:
        return f"API request failed with status code: {response.status_code}"

##################### Make custom tool ############################

from typing import Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field


##### Signal Status Tool #####
class SignalStatusInput(BaseModel):
    """Input for getting the first three stock signal based on status"""
    status: str = Field(description="User status of the signal (e.g., 'fresh buy', 'fresh sell', 'positif', 'negatif')")

class SignalStatusTool(BaseTool):
    name = "get_signals_status"
    description = """
        Fetches the first three stock signal for a given status from the API and returns it with specific, renamed keys. Use the returned information to create a list of stocks, with details pertaining to their technical analysis. Nominal values are in Indonesian rupiah. Make sure to use the right currency denomination. 

        If the user is asking about a specific company, DO NOT use this  tool. 

        Make sure to end with a note saying that this is not financial advice and that users should do their own research before buying stocks as it is a risky asset.
        """
    args_schema: Type[BaseModel] = SignalStatusInput

    def _run(self, status: str):
        # Assuming the get_first_signal_for_status function is already defined
        signal_response = get_signals_status(status)
        return signal_response

    def _arun(self, status: str):
        raise NotImplementedError("get_first_signal_for_status does not support asynchronous")
    
##### TradingInfo Tool #####
class TradingInfoInput(BaseModel):
    """Input for getting trading information based on ticker"""
    ticker: str = Field(description="Ticker symbol for which to get trading information")

class TradingInfoTool(BaseTool):
    name = "get_trading_info"
    description = """
        Useful for fetching trading information or and technical analysis for a specific public company. You should enter the stock ticker. Fetches trading information for a given ticker from the API and returns the result.

        Make sure to end with a note saying that this is not financial advice and that users should do their own research before buying stocks as it is a risky asset.
        """
    args_schema: Type[BaseModel] = TradingInfoInput

    def _run(self, ticker: str):
        # Assuming the get_trading_info function is already defined
        trading_info_response = get_trading_info(ticker)
        return trading_info_response

    def _arun(self, ticker: str):
        raise NotImplementedError("get_trading_info does not support asynchronous")
    
##### InvestInfo Tool #####
class InvestInfoInput(BaseModel):
    """Input for getting financial ratio and investment information based on ticker"""
    ticker: str = Field(description="Ticker symbol for which to get trading information")

class InvestInfoTool(BaseTool):
    name = "get_invest_info"
    description = """
        Useful for fetching financial ratio information and technical analysis for a specific public company. For example, if the query asks what their EPS growth, Price to Earnings ratio, and Book Value Per Share. You should enter the stock ticker. Fetches ratio and investment information for a given ticker from the API and returns the result.

        Use this tool when the query asks for an investment recommendation for a specific company. 

        Make sure to end with a note saying that this is not financial advice and that users should do their own research before buying stocks as it is a risky asset.
        """
    args_schema: Type[BaseModel] = InvestInfoInput

    def _run(self, ticker: str):
        # Assuming the get_trading_info function is already defined
        trading_info_response = get_invest_info(ticker)
        return trading_info_response

    def _arun(self, ticker: str):
        raise NotImplementedError("get_trading_info does not support asynchronous")
    
########################### Create Agent ##############################

# Assuming the environment setup for Langchain and OpenAI API key is done as per your example

from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(
    model='gpt-3.5-turbo-0613',
    temperature=0.3,
)

tools = [SignalStatusTool(), TradingInfoTool(), InvestInfoTool()]

agent = OpenAIFunctionsAgent.from_llm_and_tools(llm, tools)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)


#Example usage
#response = agent_executor.invoke("get first signal for status fresh buy")

#print(response)

##################### Streamlit Application ##########################

# # Title of the application
# st.title('AI-Powered Stock Analysis Tool')

# # Display example prompts with a note
# st.write("To get you started, please either copy/paste the below prompts or follow the format structure for best results.")
# example_prompts = """
# - For status-based signal analysis (not company-specific), enter a status like 'fresh buy', 'fresh sell', 'positive', or 'negative'. Example: 'Show fresh buy signals.'
# - For trading information about a specific company, enter the stock ticker. Example: 'Get trading information for BBRI.'
# - For investment information such as financial ratios or investment recommendations for a specific company, enter the stock ticker. Example: 'What are the EPS growth, Price to Earnings ratio, and Book Value Per Share for BBCA?'
# """
# st.text_area("Example Prompts:", example_prompts, height=150, key="example_prompts", disabled=True,help="Copy and paste one of these examples into the input box above or modify them to fit your specific query.")

# # Input for user queries
# user_query = st.text_area("Enter your query:", height=150)

# if user_query:
#     # Function to invoke AI agent
#     def get_response(query):
#         # Simulate invoking an external AI agent
#         try:
#             return agent_executor.invoke(query)
#         except Exception as e:
#             st.error(f"Failed to retrieve response: {e}")
#             return None

#     # Button to submit query and display the response
#     if st.button('Submit'):
#         response = get_response(user_query)
#         if response:
#             # Assuming the response is a JSON object, we need to parse it
#             try:
#                 # Assuming 'response' is already a Python dictionary
#                 if 'output' in response:
#                     output_message = response['output']
#                 else:
#                     output_message = "Output key not found in response."
#                 st.write(output_message)
#             except Exception as e:
#                 st.error(f"Error processing response: {e}")
#         else:
#             st.write("No response received.")


# Title of the application
st.title('AI-Powered Stock Analysis Tool')

# Display example prompts with a note
st.write("To get you started, please either copy/paste the below prompts or follow the format structure for best results.")
example_prompts = """
- For status-based signal analysis (not company-specific), enter a status like 'fresh buy', 'fresh sell', 'positive', or 'negative'. Example: 'Show fresh buy signals.'
- For trading information about a specific company, enter the stock ticker. Example: 'Get trading information for BBRI.'
- For investment information such as financial ratios or investment recommendations for a specific company, enter the stock ticker. Example: 'What are the EPS growth, Price to Earnings ratio, and Book Value Per Share for BBCA?'
"""
st.text_area("Example Prompts:", example_prompts, height=150, key="example_prompts", disabled=True, help="Copy and paste one of these examples into the input box above or modify them to fit your specific query.")

# Input for user queries
user_query = st.text_area("Enter your query:", height=150)

if user_query:
    # Function to invoke AI agent
    def get_response(query):
        # Simulate invoking an external AI agent
        try:
            return agent_executor.invoke(query)
        except Exception as e:
            st.error(f"Failed to retrieve response: {e}")
            return None

    response = get_response(user_query)
    if response:
        # Assuming the response is a JSON object, we need to parse it
        try:
            # Assuming 'response' is already a Python dictionary
            if 'output' in response:
                output_message = response['output']
            else:
                output_message = "Output key not found in response."
            st.write(output_message)
        except Exception as e:
            st.error(f"Error processing response: {e}")
    else:
        st.write("No response received.")
