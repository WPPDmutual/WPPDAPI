package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
	"os"

	"github.com/timpalpant/go-iex"
	"github.com/timpalpant/go-iex/iextp/deep"
)



func main() {
	for i := 1; i <= 31; i++{
	start := time.Now()
	m := make(map[string][]interface{})
	var test map[string]interface{}
	client := iex.NewClient(&http.Client{})

	// Get historical data dumps available for 2016-12-12.
	date := time.Date(2017, time.June , i, 0, 0, 0, 0, time.UTC)
	histData, err := client.GetHIST(date)
	if err != nil {
		continue
		panic(err)
	} else if len(histData) == 0 {
		panic(fmt.Errorf("Found %v available data feeds", len(histData)))
	}
	// Fetch the pcap dump for that date and iterate through its messages.
	resp, err := http.Get(histData[0].Link)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	packetDataSource, err := iex.NewPacketDataSource(resp.Body)
	if err != nil {
		panic(err)
	}
	pcapScanner := iex.NewPcapScanner(packetDataSource)


  i := 0
  msg := " "


	for msg != ""{
		msg, err := pcapScanner.NextMessage()
		if err != nil {
			if err == io.EOF {
				break
			}

			panic(err)
		}
		switch msg := msg.(type) {
		case *deep.TradeReportMessage:
			buf, _ := json.Marshal(msg)
			json.Unmarshal(buf, &test)
			ticker := test["Symbol"].(string)
			m[ticker] = append(m[ticker], make(map[string]interface{}))
				hm := m[ticker][len(m[ticker])-1].(map[string]interface{})
				hm["Price"] = test["Price"]
				hm["Timestamp"] = test["Timestamp"]
				m[ticker][len(m[ticker])-1] = hm

				i++
		default:
		}
	}
	os.Mkdir("StockData/" + date.Format("2006-01-02"), 0777)
	for k := range m {
		jsonFile, _ := os.Create("StockData/" + date.Format("2006-01-02") + "/" + string(k) +".json")
		enc := json.NewEncoder(jsonFile)
		enc.Encode(m[string(k)])
		//fmt.Println(string(k))
	}

fmt.Println("Hello, I am done")
t := time.Now()
fmt.Print(t.Sub(start))
}
}
