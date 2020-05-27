def check_channels(text_channels):
		n_channels = len(text_channels)
		poll_tuple = (False, False)
		events_tuple = (False, False)
		games_tuple = (False, False)
		for p in range(n_channels):
			if "poll-channel" == text_channels[p].name:
				poll_tuple = (text_channels[p].name, text_channels[p].id)
			if "events-channel" == text_channels[p].name:
				events_tuple = (text_channels[p].name, text_channels[p].id)
			if "games-channel" == text_channels[p].name:
				games_tuple = (text_channels[p].name, text_channels[p].id)
		return (poll_tuple, events_tuple, games_tuple)

def check_basic_channels(text_channels):
		n_channels = len(text_channels)
		spam_tuple = (False, False)
		bot_psa_tuple = (False, False)
		for p in range(n_channels):
			if "spam" == text_channels[p].name:
				spam_tuple = (text_channels[p].name, text_channels[p].id)
			if "bot-channel" == text_channels[p].name:
				bot_psa_tuple = (text_channels[p].name, text_channels[p].id)
		return (spam_tuple, bot_psa_tuple)				