image:
	@cd jqtransformation && gcloud builds submit --tag gcr.io/ultra-hologram-297914/jqt
	@cd mongodbtarget && gcloud builds submit --tag gcr.io/ultra-hologram-297914/mongodbtarget

apply:
	@cd jqtransformation/config && kubectl apply -f 100-registration.yaml
	@cd mongodbtarget/config && kubectl apply -f 100-registration.yaml

lint:
	@cd jqtransformation/pkg/adapter && golangci-lint run
	@cd jqtransformation/cmd && golangci-lint run
	@cd mongodbtarget/pkg/adapter && golangci-lint run
	@cd mongodbtarget/cmd && golangci-lint run
