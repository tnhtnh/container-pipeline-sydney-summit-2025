package main

import (
        "bytes"
        "encoding/json"
        "net/http"
        "net/http/httptest"
        "os"
        "os/exec"
        "testing"
)

// TestIndexEndpoint tests the index endpoint
func TestIndexEndpoint(t *testing.T) {
        // Set the GIT_SHA environment variable for testing
        testSHA := "test1234"
        os.Setenv("GIT_SHA", testSHA)
        defer os.Unsetenv("GIT_SHA")

        // Create a request to the index endpoint
        req, err := http.NewRequest("GET", "/", nil)
        if err != nil {
                t.Fatal(err)
        }

        // Create a ResponseRecorder to record the response
        rr := httptest.NewRecorder()
        handler := http.HandlerFunc(indexHandler)

        // Call the handler
        handler.ServeHTTP(rr, req)

        // Check status code
        if status := rr.Code; status != http.StatusOK {
                t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
        }

        // Parse response data
        var response MessageResponse
        if err := json.Unmarshal(rr.Body.Bytes(), &response); err != nil {
                t.Fatal(err)
        }

        // Verify message contains git SHA
        if response.Message == "" {
                t.Errorf("handler returned empty message")
        }
        if response.Message != "Application version: "+testSHA {
                t.Errorf("handler returned unexpected message: got %v want %v", 
                        response.Message, "Application version: "+testSHA)
        }
}

// TestHealthcheckEndpoint tests the healthcheck endpoint
func TestHealthcheckEndpoint(t *testing.T) {
        // Create a request to the healthcheck endpoint
        req, err := http.NewRequest("GET", "/healthcheck", nil)
        if err != nil {
                t.Fatal(err)
        }

        // Create a ResponseRecorder to record the response
        rr := httptest.NewRecorder()
        handler := http.HandlerFunc(healthcheckHandler)

        // Call the handler
        handler.ServeHTTP(rr, req)

        // Check status code
        if status := rr.Code; status != http.StatusOK {
                t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
        }

        // Parse response data
        var response StatusResponse
        if err := json.Unmarshal(rr.Body.Bytes(), &response); err != nil {
                t.Fatal(err)
        }

        // Verify response content
        if response.Status != "OK" {
                t.Errorf("handler returned unexpected status: got %v want %v", response.Status, "OK")
        }
}

// TestSummitEndpoint tests the summit endpoint
func TestSummitEndpoint(t *testing.T) {
        // Create a request to the summit endpoint
        req, err := http.NewRequest("GET", "/summit", nil)
        if err != nil {
                t.Fatal(err)
        }

        // Create a ResponseRecorder to record the response
        rr := httptest.NewRecorder()
        handler := http.HandlerFunc(summitHandler)

        // Call the handler
        handler.ServeHTTP(rr, req)

        // Check status code
        if status := rr.Code; status != http.StatusOK {
                t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
        }

        // Parse response data
        var response MessageResponse
        if err := json.Unmarshal(rr.Body.Bytes(), &response); err != nil {
                t.Fatal(err)
        }

        // Verify response content
        expectedMessage := "I hope you are enjoying this talk"
        if response.Message != expectedMessage {
                t.Errorf("handler returned unexpected message: got %v want %v", response.Message, expectedMessage)
        }
}

// TestRunCommandEndpoint tests the run_command endpoint
func TestRunCommandEndpoint(t *testing.T) {
        // Save the original exec.Command and restore it after the test
        originalExecCommand := execCommand
        defer func() { execCommand = originalExecCommand }()

        // Mock the exec.Command to return a known value
        execCommand = func(command string, args ...string) *exec.Cmd {
                return fakeExecCommand("command output")
        }

        // Prepare the test data with a simple command
        testData := CommandRequest{Command: "ls -la"}
        jsonData, err := json.Marshal(testData)
        if err != nil {
                t.Fatal(err)
        }

        // Create a request to the run_command endpoint
        req, err := http.NewRequest("POST", "/run_command", bytes.NewBuffer(jsonData))
        if err != nil {
                t.Fatal(err)
        }
        req.Header.Set("Content-Type", "application/json")

        // Create a ResponseRecorder to record the response
        rr := httptest.NewRecorder()
        handler := http.HandlerFunc(runCommandHandler)

        // Call the handler
        handler.ServeHTTP(rr, req)

        // Check status code
        if status := rr.Code; status != http.StatusOK {
                t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
        }

        // Parse response data
        var response CommandResponse
        if err := json.Unmarshal(rr.Body.Bytes(), &response); err != nil {
                t.Fatal(err)
        }

        // Verify response content
        if response.Result != "command output" {
                t.Errorf("handler returned unexpected result: got %v want %v", response.Result, "command output")
        }
}

// TestRunCommandInjectionScenario tests the command injection vulnerability
func TestRunCommandInjectionScenario(t *testing.T) {
        // Save the original exec.Command and restore it after the test
        originalExecCommand := execCommand
        defer func() { execCommand = originalExecCommand }()

        // Mock the exec.Command to return a known value
        execCommand = func(command string, args ...string) *exec.Cmd {
                return fakeExecCommand("sensitive data")
        }

        // Prepare test data with a command that includes command injection
        maliciousCommand := "echo 'hello' && cat /etc/passwd"
        testData := CommandRequest{Command: maliciousCommand}
        jsonData, err := json.Marshal(testData)
        if err != nil {
                t.Fatal(err)
        }

        // Create a request to the run_command endpoint
        req, err := http.NewRequest("POST", "/run_command", bytes.NewBuffer(jsonData))
        if err != nil {
                t.Fatal(err)
        }
        req.Header.Set("Content-Type", "application/json")

        // Create a ResponseRecorder to record the response
        rr := httptest.NewRecorder()
        handler := http.HandlerFunc(runCommandHandler)

        // Call the handler
        handler.ServeHTTP(rr, req)

        // Check status code
        if status := rr.Code; status != http.StatusOK {
                t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
        }

        // Parse response data
        var response CommandResponse
        if err := json.Unmarshal(rr.Body.Bytes(), &response); err != nil {
                t.Fatal(err)
        }

        // Verify response content
        if response.Result != "sensitive data" {
                t.Errorf("handler returned unexpected result: got %v want %v", response.Result, "sensitive data")
        }
}

// Mock for exec.Command
var execCommand = exec.Command

// fakeExecCommand returns a fake exec.Command that outputs the given output
func fakeExecCommand(output string) *exec.Cmd {
        return exec.Command("echo", output)
}