publish:
	rsync -rlptoDvog --delete --chown=ubuntu:ubuntu --exclude '.git*' . namenode:project
