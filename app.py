import requests
from bs4 import BeautifulSoup
import dash
from dash.dependencies import Input, Output, State

import layout
import json

app = dash.Dash(__name__)
server = app.server
app.layout = layout.layout

def show_mindmap():
    @app.callback(Output('cytoscape', 'elements'),
                  [
                      Input('cytoscape', 'tapNodeData'),
                      Input('submit-button-state', 'n_clicks'),
                      Input('input1', 'value'),
                      Input('input2', 'value'),
                      Input('input3', 'value'),
                      Input('input4', 'value'),
                      Input('input5', 'value'),
                      Input('input6', 'value'),
                      Input('input7', 'value')
                  ]
                   )
    def update_node(tap_check, n_clicks, company, from_date, dest_date, issue_count, keyword_prob, keyword_count, industry_count):

        if not tap_check and n_clicks == 1 and company:
            return [{'data': {'id': company, 'label': company, 'firstname': company}}]

        if tap_check or from_date or dest_date or issue_count or keyword_prob or keyword_count or industry_count:
            print(company, from_date, dest_date, issue_count, keyword_prob, keyword_count, industry_count)
            return response(company, from_date, dest_date, float(issue_count), float(keyword_prob), int(keyword_count), industry_count)

        return []

    def soup_html(api):
        url = 'https://api.deepsearch.com/v1/compute?input={0}'
        response = requests.get(url.format(api), headers={'Authorization':
                                                                 'Basic OWI0OTA5NGQ1MDA1NDIzZGFiZDVmZDNlNzk3OTI5MmM6ZjkzYmMxYmYzM2ViYWRlYTk0YmZjNDQxNzQyMDA1ODAwMjBhMzdlMDQwMzI0YTZhNTlmNmJmNjYzZWRkOGUyZg=='})
        soup = BeautifulSoup(response.text, 'lxml')
        return json.loads(soup.text)['data']['pods'][1]['content']['data']

    def response(company, from_date, dest_date, issue_count, keyword_prob, keyword_count, industry_count):
        news_category = '["economy", "society", "culture", "world", "tech", "entertainment"]'
        sector = 'DocumentAggregation(["news"], {0}, "{1}", "named_entities.entities.company.name:{2}", date_from={3}, date_to={4})'.format(news_category, company, industry_count, from_date, dest_date)
        related_company = soup_html(sector)['key']

        histories = 'SearchHistoricalTopics(["news"],{0},"{1}", date_from={2}, date_to={3})'.format(news_category, company, from_date, dest_date)
        temp = soup_html(histories)['topics']
        related_topic_title = list()
        for content in temp:
            if issue_count <= content['score']:
                related_topic_title.append(content['topic'])

        similar = 'SimilarKeywords("{0}", min_score={1}, date_from={2}, date_to={3})'.format(company, keyword_prob, from_date[:4], dest_date[:4])
        related_keywords = list(set(soup_html(similar)['keyword']))
        standard = min(len(related_keywords), keyword_count)
        related_keywords = related_keywords[:standard]

        result = list()
        result.extend([{'data': {'id': com, 'label': com}, 'style': {'background-color': 'blue', 'font-size': '6px'}} for com in related_company])
        result.extend([{'data': {'id': topic, 'label': topic}, 'style': {'background-color': 'red', 'font-size': '6px'}} for topic in related_topic_title])
        result.extend([{'data': {'id': keywords, 'label': keywords}, 'style': {'background-color': 'green', 'font-size': '6px'}} for keywords in related_keywords])

        result.extend([{'data': {'source': company, 'target': com}} for com in related_company])
        result.extend([{'data': {'source': company, 'target': topic}} for topic in related_topic_title])
        result.extend([{'data': {'source': company, 'target': keywords}} for keywords in related_keywords])

        return result

show_mindmap()
if __name__ == '__main__':
    app.run_server(debug=True)