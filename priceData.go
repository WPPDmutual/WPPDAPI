package main

import (
	"encoding/json"
	"encoding/csv"
	"fmt"
	"io"
	"net/http"
	"time"
	"os"
	"io/ioutil"
	"strconv"

	"gopkg.in/cheggaaa/pb.v1"
	"github.com/timpalpant/go-iex"
)



func main() {

	//Multiplier determines how many seconds are in each csv interval

	multiplier := 1

	//All tickers to search for, I recommend not simply parsing all available tickers as it would dramatically increase file size with little increase in genuinely useful data

	tickers := []string{"A", "AAL", "AAP", "AAPL", "ABBV", "ABC", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADS", "ADSK", "AEE", "AEP", "AES", "AET", "AFL", "AGN", "AIV", "AIZ", "AJG", "AKAM", "ALB", "ALK", "ALL", "ALLE", "ALXN", "AMAT", "AMD", "AME", "AMG", "AMGN", "AMP", "AMT", "AMZN", "AN", "ANTM", "AON", "APA", "APC", "APD", "APH", "ARE", "ARNC", "ATVI", "AVB", "AVY", "AWK", "AXP", "AYI", "AZO", "BA", "BAC", "BAX", "BBBY", "BBT", "BBY", "BCR", "BDX", "BEN", "BIIB", "BK", "BLK", "BLL", "BMY", "BSX", "BWA", "BXP", "C", "CA", "CAG", "CAH", "CAT", "CB", "CBOE", "CBS", "CCI", "CCL", "CELG", "CERN", "CF", "CFG", "CHD", "CHK", "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COG", "COL", "COO", "COP", "COST", "COTY", "CPB", "CRM", "CSCO", "CSX", "CTAS", "CTL", "CTSH", "CTXS", "CVS", "CVX", "D", "DAL", "DE", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DISCA", "DISCK", "DISH", "DOV", "DPS", "DRI", "DTE", "DUK", "DVA", "DVN", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL", "EMN", "EMR", "EOG", "EQIX", "EQR", "EQT", "ESRX", "ESS", "ETFC", "ETN", "EXC", "EXPD", "EXPE", "EXR", "F", "FAST", "FB", "FBHS", "FCX", "FDX", "FE", "FFIV", "FIS", "FISV", "FITB", "FL", "FLIR", "FLR", "FLS", "FMC", "FOX", "FOXA", "FRT", "FSLR", "GD", "GE", "GGP", "GILD", "GIS", "GLW", "GM", "GOOG", "GPC", "GPN", "GPS", "GRMN", "GS", "GT", "GWW", "HAL", "HAS", "HBAN", "HBI", "HCA", "HCP", "HD", "HES", "HIG", "HOG", "HOLX", "HP", "HRB", "HRL", "HRS", "HSIC", "HST", "HSY", "HUM", "IBM", "ICE", "IFF", "ILMN", "INCY", "INTC", "INTU", "IP", "IPG", "IR", "ISRG", "IT", "ITW", "IVZ", "JCI", "JEC", "JNJ", "JNPR", "JPM", "JWN", "K", "KEY", "KLAC", "KMB", "KMI", "KMX", "KO", "KORS", "KR", "KSS", "KSU", "L", "LB", "LEG", "LEN", "LH", "LKQ", "LLL", "LLY", "LMT", "LNT", "LOW", "LRCX", "LUK", "LUV", "LYB", "M", "MA", "MAA", "MAC", "MAR", "MAS", "MAT", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "MHK", "MKC", "MLM", "MMC", "MMM", "MNK", "MNST", "MO", "MON", "MOS", "MPC", "MRK", "MRO", "MS", "MSFT", "MSI", "MTB", "MU", "MUR", "NAVI", "NBL", "NDAQ", "NEE", "NEM", "NFLX", "NFX", "NI", "NKE", "NLSN", "NOC", "NOV", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NWL", "NWS", "NWSA", "O", "OKE", "OMC", "ORCL", "ORLY", "OXY", "PAYX", "PBCT", "PCAR", "PCG", "PDCO", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKI", "PLD", "PM", "PNC", "PNR", "PNW", "PPG", "PPL", "PRGO", "PRU", "PSX", "PVH", "PWR", "PX", "PXD", "QCOM", "QRVO", "RCL", "REG", "REGN", "RF", "RHI", "RHT", "RIG", "RJF", "RL", "ROK", "ROP", "ROST", "RRC", "RSG", "RTN", "SBUX", "SCG", "SCHW", "SEE", "SHW", "SIG", "SJM", "SLB", "SLG", "SNA", "SNI", "SNPS", "SO", "SPGI", "SRCL", "SRE", "STI", "STT", "STX", "STZ", "SWK", "SWKS", "SYF", "SYK", "SYMC", "SYY", "T", "TAP", "TDC", "TDG", "TGT", "TIF", "TJX", "TMK", "TMO", "TRIP", "TROW", "TRV", "TSCO", "TSN", "TSS", "TWX", "TXN", "TXT", "UA", "UAA", "UAL", "UDR", "UHS", "ULTA", "UNH", "UNM", "UNP", "UPS", "URI", "USB", "UTX", "V", "VAR", "VFC", "VIAB", "VLO", "VMW", "VRSK", "VRSN", "VRTX", "VTR", "VZ", "WAT", "WDC", "WEC", "WFC", "WHR", "WLTW", "WM", "WMB", "WMT", "WU", "WY", "WYN", "WYNN", "XEL", "XL", "XLNX", "XOM", "XRAY", "XRX", "XYL", "YUM", "ZBH", "ZION", "ZNGA", "ZTS"}


	//This function below checks whether the ticker is traded on IEX, the above tickers have already been checked thus there is no need to waist time on this
	// tickers = removeUnlisted(tickers)

	layout := "2006-01-02T15:04:05.000000000Z"

	fmt.Println("Starting Parsing")

	// number of dase you want to parse

	days := 250

	for i := 0; i <= days; i++{
	start := time.Now()

	var test map[string]interface{}
	client := iex.NewClient(&http.Client{})

	date := time.Date(2017, time.May, 15, 0, 0, 0, 0, time.UTC).AddDate(0, 0, i)

	if(date.Sub(start) > 0){
		fmt.Println("Done")
		break
	}


	if (date.Weekday() == 6 || date.Weekday() == 7) {
		continue
	}

	// Get historical data dumps available for 2016-12-12.

	final := make([][]string , 6.5*3600/multiplier+1)


	for i := 0; i < len(final); i++ {
		d := date.Add(time.Hour * 13).Add(time.Minute * 30).Add(time.Second * time.Duration(i*multiplier)).Format(time.RFC3339)
		final[i] = make([]string, len(tickers)+1)
		final[i][0] = d
	}


	duration := "2y"

	switch {
	case date.Sub(start.AddDate(0, -1, 0)) > 0:
		duration = "1m"
	case date.Sub(start.AddDate(0, -3, 0)) > 0:
		duration = "3m"
	case date.Sub(start.AddDate(0, -6, 0)) > 0:
		duration = "6m"
	case date.Sub(start.AddDate(-1, 0, 0)) > 0:
		duration = "1y"
	case date.Sub(start.AddDate(-2, 0, 0)) > 0:
		duration = "2y"
	}

	closed := make([]string, len(final[len(final)-1]))

	closed[0] = final[len(final)-1][0]

	for k, value := range tickers{
		oc := getOpenClose(value, date.Format("2006-01-02"), duration)
		final[0][k+1] = oc[0]
		closed[k+1] = oc[1]
	}

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

  msg := " "

	var a int = 1

	fmt.Print("Parsing ")
	fmt.Println(date)


	open := false

	bar := pb.StartNew(len(final) - 1)

	for msg != ""{
		msg, err := pcapScanner.NextMessage()
		if err != nil {
			if err == io.EOF {
				break
			}

			panic(err)
		}

		buf, _ := json.Marshal(msg)
		json.Unmarshal(buf, &test)

		MessageType := int(test["MessageType"].(float64))

		t, _ := time.Parse(layout, test["Timestamp"].(string))
		d := date.Add(time.Hour * 13).Add(time.Minute * 30).Add(time.Second * time.Duration(a*multiplier))


		if(t.Sub(d.Add(time.Second * time.Duration(multiplier))) > 0){

			final[a] = removeNil(final, a)

			bar.Increment()
			a++
		}

		if MessageType == 83 && int(test["SystemEvent"].(float64)) == 82 {
			open = true
		}

		if MessageType == 83 && int(test["SystemEvent"].(float64)) == 77{

			open = false

			bar.Finish()
			break

		}

		if MessageType == 84 {

					ticker := test["Symbol"].(string)

					if open == true {
						if pos(ticker, tickers) > -1 {
							final[a][pos(ticker, tickers) + 1] = strconv.FormatFloat(test["Price"].(float64), 'f', -1, 64)
						}
					}

		}
	}

	final[len(final) - 1] = closed


	headers := make([][]string, 1)
	headers[0] = append([]string{"Timestamp"}, tickers...)

	fileString := append(headers, final...)

	file, err := os.Create("csvData/" + date.Format("2006-01-02") + ".csv")
  defer file.Close()

  if err != nil {
      os.Exit(1)
  }

  csvWriter := csv.NewWriter(file)
  csvWriter.WriteAll(fileString)
  csvWriter.Flush()


	fmt.Print("Finished in ")
	t := time.Now()
	fmt.Println(t.Sub(start))
}
}

func pos(value string, slice []string) int {
	for p, v := range slice {
		if v == value {
			return p
		}
	}
	return -1
}

func getOpenClose(ticker string, date string, duration string) []string{
	response, _ := http.Get("https://api.iextrading.com/1.0/stock/"+ ticker + "/chart/" + duration)

	var m []map[string]interface{}

	defer response.Body.Close()
	contents, _ := ioutil.ReadAll(response.Body)

	json.Unmarshal(contents, &m)

	open := 0.0
	close := 0.0

	for _, value := range m{
		if(value["date"].(string) == date){
			 	open = value["open"].(float64)
				close = value["close"].(float64)
		}
	}

	final := []string{strconv.FormatFloat(open, 'f', -1, 64), strconv.FormatFloat(close, 'f', -1, 64)}

	return final
}

func removeUnlisted(tickers []string) []string{
for k, value := range tickers{
	response, err := http.Get("https://api.iextrading.com/1.0/stock/" + value + "/company")
	if err != nil {
			fmt.Printf("%s", err)
			os.Exit(1)
	} else {
			defer response.Body.Close()
			contents, err := ioutil.ReadAll(response.Body)
			if err != nil {
					fmt.Printf("%s", err)
					os.Exit(1)
			}
			if(string(contents) == "Unknown symbol"){
				fmt.Print("Removed ")
				fmt.Println(value)
				tickers = append(tickers[:k], tickers[k+1:]...)
			}
	}
}
return tickers
}

func removeNil(final [][]string, a int) []string{
		for pos("", final[a]) != -1{
			position := pos("", final[a])
			final[a][position] = final[a-1][position]
		}
		return final[a]
}

func checkError(message string, err error) {
    if err != nil {
        fmt.Println(message, err)
    }
}
