
run_ansible_install: projenv/bin/activate Makefile
	ansible-playbook -i inv.yml hodor_base_playbook.yml
	# . projenv/bin/activate && ansible-playbook -i inv.yml hodor_base_playbook.yml

# not really used, just to remind myself how ad hoc commands are run
run_ansible_adhoc_hostname: projenv/bin/activate Makefile
	. projenv/bin/activate && ansible -i inv.yml all -u pi -b -a hostname

# The following builds a project-specific environment
# with Ansible installed for use by the commands above.
# To use the environment, use:
#
#    . projenv/bin/activate
#
# projenv/bin/activate: Makefile
	# mkdir -p projenv
	# virtualenv projenv
	# . projenv/bin/activate && pip install --upgrade pip
	# . projenv/bin/activate && pip install -r requirements.txt
