package main

import (
	"fmt"
)

func main() {
	isLoggedIn := true
	fmt.Println(isLoggedIn)

	isLoggedIn = false
	fmt.Println(isLoggedIn)

	var isLoggedout bool = true
	isLoggedout = false
	fmt.Println(isLoggedout)
}
