
#### COMMMON FUNCTIONS ####

def prompt_def(var, askmsg, default)
  set(var) do
	Capistrano::CLI.ui.ask "#{askmsg} [#{default}] : "
  end
  set var, default if eval("#{var.to_s}.empty?")
end

