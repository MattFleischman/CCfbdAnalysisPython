import pandas as pd


def transform_performing_player_recruiting():
    #TODO need to test more thoroughly and run multi var reg comparison with gross permission group rankings vs wins/points
    data_directory = 'C:/Users/mattf/cfbd_analytics/file_stage/'
    df_player_stats = pd.read_csv(f'{data_directory}players_get_player_season_stats_data_extract_2022111523.txt',
                                  sep='|')
    df_roster = pd.read_csv(f'{data_directory}teams_get_roster_data_extract_2022111523.txt', sep='|')
    df_recruits = pd.read_csv(f'{data_directory}recruiting_get_recruiting_players_data_extract_2022111610.txt', sep='|')
    df_transfer_portal = pd.read_csv(f'{data_directory}players_get_transfer_portal_data_extract_2022111523.txt',
                                     sep='|')

    df_roster['first_recruit_id'] = df_roster['recruit_ids'].apply(
        lambda x: x[1:-1].split(',')[0] if (len(x[1:-1].split(',')) > 1) else x[1:-1])

    df_recruits['last_name'] = df_recruits['name'].str.split(' ', expand=True)[1]
    df_recruits['id'] = df_recruits['id'].apply(str)

    df_recruits = df_recruits[
        ['name', 'last_name', 'id', 'athlete_id', 'recruit_type', 'year', 'ranking', 'stars', 'rating',
         'committed_to', 'state_province']]

    df_transfer_portal['id'] = None
    df_transfer_portal['athlete_id'] = None
    df_transfer_portal['recruit_type'] = None
    df_transfer_portal['ranking'] = None
    df_transfer_portal['state_province'] = None

    df_transfer_portal['name'] = df_transfer_portal['first_name'] + " " + df_transfer_portal['last_name']
    df_transfer_portal = df_transfer_portal[
        ['name', 'last_name', 'id', 'athlete_id', 'recruit_type', 'season', 'ranking', 'stars', 'rating',
         'destination', 'state_province']]
    df_transfer_portal.rename({'season': 'year', 'destination': 'committed_to'}, inplace=True)

    df_recruits_expanded = pd.concat([df_recruits, df_transfer_portal], ignore_index=True)

    roster_missing_id = df_roster.loc[df_roster['first_recruit_id'] == '']
    roster_including_id = df_roster.loc[df_roster['first_recruit_id'] != '']

    main_recruiting_rosters_df = roster_including_id.merge(df_recruits_expanded, 'inner',
                                                           left_on=['team', 'first_recruit_id'],
                                                           right_on=['committed_to', 'id'])

    secondary_recruiting_rosters_df = roster_missing_id.merge(df_recruits_expanded, 'inner',
                                                              left_on=['team', 'last_name', 'home_state'],
                                                              right_on=['committed_to', 'last_name',
                                                                        'state_province'])

    combined_recruiting_rosters_df_new = pd.concat([main_recruiting_rosters_df, secondary_recruiting_rosters_df],
                                                   ignore_index=True)

    recruited_players_w_stats = combined_recruiting_rosters_df_new.loc[
        combined_recruiting_rosters_df_new.id_x.isin(df_player_stats.player_id.values.tolist())]

    return recruited_players_w_stats[['team', 'position', 'stars', 'rating', 'ranking']].groupby(['team']).mean()

