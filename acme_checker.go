package main

import (
	"bufio"
	"fmt"
	"log"
	"os"

	"github.com/miekg/dns"
)

func getCNAME(domain string) (string, error) {
	c := dns.Client{}
	m := dns.Msg{}
	m.SetQuestion(dns.Fqdn("_acme-challenge."+domain), dns.TypeCNAME)

	r, _, err := c.Exchange(&m, "8.8.8.8:53") // Using Google's public DNS server
	if err != nil {
		return "", err
	}
	if len(r.Answer) < 1 {
		return "CNAME record missing", nil
	}

	for _, ans := range r.Answer {
		if t, ok := ans.(*dns.CNAME); ok {
			return t.Target, nil
		}
	}
	return "CNAME record missing", nil
}

func main() {
	file, err := os.Open("acme_list.txt")
	if err != nil {
		log.Fatalf("Failed to open file: %s", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		domain := scanner.Text()
		cname, err := getCNAME(domain)
		if err != nil {
			fmt.Printf("Error querying CNAME for %s: %s\n", domain, err)
			continue
		}
		fmt.Printf("CNAME for _acme-challenge.%s is %s\n", domain, cname)
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("Error reading file: %s", err)
	}
}

