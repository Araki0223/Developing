1// 先ほど生成したURL
const url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1009993429057254143'

$.getJSON(url, (data) => {
    console.log(data.result);
});